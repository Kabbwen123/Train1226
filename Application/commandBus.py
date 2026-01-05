# commandbus_named.py
from __future__ import annotations
import os, time, threading, queue
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future
from typing import Any, Callable, Dict, Optional, Tuple, Type

# =============================
# 执行策略
# =============================
@dataclass
class ExecPolicy:
    executor: str = "inline"   # 'inline' | 'thread' | 'process'
    timeout: Optional[float] = None
    exclusive_key: Optional[Callable[[Any], Optional[str]]] = None  # 同资源互斥/串行（对 named 传 kwargs，对 dc 传 cmd）
    ordered: bool = False  # True 则对同一 key 启用 FIFO（用 SerialExecutor 实现）

# =============================
# 有序串行执行器（每 key 一个）
# =============================
class SerialExecutor:
    """单线程按 FIFO 顺序执行提交的可调用对象。submit 返回 Future。"""
    def __init__(self) -> None:
        self._q: "queue.Queue[Tuple[Callable[[], Any], Future]]" = queue.Queue()
        self._t = threading.Thread(target=self._run, daemon=True)
        self._t.start()

    def submit(self, fn: Callable[[], Any]) -> Future:
        fut: Future = Future()
        self._q.put((fn, fut))
        return fut

    def _run(self) -> None:
        while True:
            fn, fut = self._q.get()
            try:
                if fut.set_running_or_notify_cancel():
                    fut.set_result(fn())
            except Exception as e:
                fut.set_exception(e)

# 顶层适配：给进程池用 kwargs 调用任务函数
def _call_with_kwargs(func: Callable[..., Any], kwargs: Dict[str, Any]) -> Any:
    return func(**kwargs)

# =============================
# CommandBus（命名命令为主；兼容 dataclass 命令）
# =============================
class CommandBus:
    _class_lock = threading.RLock()

    # 命名命令注册表
    _class_named_handlers: Dict[str, Tuple[Callable[..., Any], ExecPolicy]] = {}
    _class_named_process: Dict[str, Tuple[Callable[..., Any], ExecPolicy]] = {}

    # dataclass 命令注册表（兼容）
    _class_handlers_dc: Dict[Type[Any], Tuple[Callable[[Any], Any], ExecPolicy]] = {}
    _class_process_dc: Dict[Type[Any], Tuple[Callable[[Any], Any], ExecPolicy]] = {}

    def __init__(self, thread_workers: int = 8, process_workers: int = os.cpu_count() or 2) -> None:
        self._lock = threading.RLock()
        self._tpool = ThreadPoolExecutor(max_workers=thread_workers, thread_name_prefix="cmd-th")
        self._ppool = ProcessPoolExecutor(max_workers=process_workers)

        # 实例态快照（可不拷贝，直接用类级表也行；这里做快照便于未来实例隔离）
        with self._class_lock:
            self._named_handlers = dict(type(self)._class_named_handlers)
            self._named_process  = dict(type(self)._class_named_process)
            self._handlers_dc    = dict(type(self)._class_handlers_dc)
            self._process_dc     = dict(type(self)._class_process_dc)

        self._key_locks: Dict[str, threading.Lock] = {}
        self._serial_execs: Dict[str, SerialExecutor] = {}

    # ---------- 命名命令：装饰器 ----------
    @classmethod
    def handler(cls, name: str, *, executor: str = "inline",
                key: Optional[Callable[[Dict[str, Any]], Optional[str]]] = None,
                ordered: bool = False, timeout: Optional[float] = None):
        """注册“命名命令”（推荐）。
        用法：@CommandBus.handler("save_to_disk", executor="thread", key=lambda kw: kw["path"], ordered=True)
        """
        pol = ExecPolicy(executor=executor, timeout=timeout, exclusive_key=key, ordered=ordered)
        def deco(fn: Callable[..., Any]):
            with cls._class_lock:
                cls._class_named_handlers[name] = (fn, pol)
            return fn
        return deco

    @classmethod
    def process_task(cls, name: str, *, task_fn: Callable[..., Any],
                     timeout: Optional[float] = None,
                     key: Optional[Callable[[Dict[str, Any]], Optional[str]]] = None,
                     ordered: bool = False):
        """注册“命名命令”的进程池任务（task_fn 必须是模块顶层）。"""
        pol = ExecPolicy(executor="process", timeout=timeout, exclusive_key=key, ordered=ordered)
        def deco(dummy: Callable[..., Any]):
            with cls._class_lock:
                cls._class_named_process[name] = (task_fn, pol)
            return dummy
        return deco

    # ---------- dataclass 命令：兼容接口（已重命名） ----------
    @classmethod
    def handler_dc(cls, cmd_type: Type[Any], policy: ExecPolicy = ExecPolicy()):
        """兼容旧版 dataclass 命令。"""
        def deco(fn: Callable[[Any], Any]):
            with cls._class_lock:
                cls._class_handlers_dc[cmd_type] = (fn, policy)
            return fn
        return deco

    @classmethod
    def process_task_dc(cls, cmd_type: Type[Any], *, task_fn: Callable[[Any], Any],
                        policy: ExecPolicy = ExecPolicy(executor="process")):
        """兼容旧版 dataclass 进程池任务。"""
        def deco(dummy: Callable[[Any], Any]):
            with cls._class_lock:
                cls._class_process_dc[cmd_type] = (task_fn, policy)
            return dummy
        return deco

    # ---------- 绑定（如需动态导入后刷新实例快照） ----------
    def bind_class_handlers(self) -> None:
        with self._lock, self._class_lock:
            self._named_handlers.update(type(self)._class_named_handlers)
            self._named_process.update(type(self)._class_named_process)
            self._handlers_dc.update(type(self)._class_handlers_dc)
            self._process_dc.update(type(self)._class_process_dc)

    # ---------- 命名命令：调用 ----------
    def handle(self, name: str, /, **kwargs) -> Any:
        """阻塞执行命名命令。"""
        spec = self._resolve_named(name)
        if spec is None:
            raise KeyError(f"No named handler for '{name}'")
        kind, (fn, pol) = spec

        key = pol.exclusive_key(kwargs) if callable(pol.exclusive_key) else None

        if kind == "process":
            submit = lambda: self._ppool.submit(_call_with_kwargs, fn, kwargs)
            if pol.ordered and key:
                sex = self._serial_execs.setdefault(key, SerialExecutor())
                return sex.submit(lambda: submit().result(pol.timeout)).result()
            f = submit()
            return f.result(timeout=pol.timeout) if pol.timeout else f.result()

        def call():
            if key:
                with self._lock:
                    lk = self._key_locks.setdefault(key, threading.Lock())
                with lk:
                    return fn(**kwargs)
            return fn(**kwargs)

        if kind == "thread":
            if pol.ordered and key:
                sex = self._serial_execs.setdefault(key, SerialExecutor())
                fut = sex.submit(call)
                return fut.result(timeout=pol.timeout) if pol.timeout else fut.result()
            fut = self._tpool.submit(call)
            return fut.result(timeout=pol.timeout) if pol.timeout else fut.result()

        # inline
        return call()

    def handle_future(self, name: str, /, **kwargs) -> Future:
        """非阻塞执行命名命令，返回 Future。"""
        spec = self._resolve_named(name)
        if spec is None:
            raise KeyError(f"No named handler for '{name}'")
        kind, (fn, pol) = spec

        key = pol.exclusive_key(kwargs) if callable(pol.exclusive_key) else None

        if kind == "process":
            submit = lambda: self._ppool.submit(_call_with_kwargs, fn, kwargs)
            if pol.ordered and key:
                sex = self._serial_execs.setdefault(key, SerialExecutor())
                return sex.submit(lambda: submit().result(pol.timeout))
            return submit()

        def call():
            if key:
                with self._lock:
                    lk = self._key_locks.setdefault(key, threading.Lock())
                with lk:
                    return fn(**kwargs)
            return fn(**kwargs)

        if kind == "thread":
            if pol.ordered and key:
                sex = self._serial_execs.setdefault(key, SerialExecutor())
                return sex.submit(call)
            return self._tpool.submit(call)

        # inline -> 也包装成线程池任务，得到 Future
        return self._tpool.submit(call)

    # ---------- dataclass 命令：兼容调用 ----------
    def handle_obj(self, cmd: Any) -> Any:
        """阻塞（dataclass 命令兼容）。"""
        spec = self._resolve_obj(cmd)
        if spec is None:
            raise KeyError(f"No handler for {type(cmd).__name__}")
        kind, (fn, pol) = spec
        key = pol.exclusive_key(cmd) if callable(pol.exclusive_key) else None

        if kind == "process":
            submit = lambda: self._ppool.submit(fn, cmd)
            if pol.ordered and key:
                sex = self._serial_execs.setdefault(key or "", SerialExecutor())
                return sex.submit(lambda: submit().result(pol.timeout)).result()
            f = submit()
            return f.result(timeout=pol.timeout) if pol.timeout else f.result()

        def call():
            if key:
                with self._lock:
                    lk = self._key_locks.setdefault(key, threading.Lock())
                with lk:
                    return fn(cmd)
            return fn(cmd)

        if kind == "thread":
            if pol.ordered and key:
                sex = self._serial_execs.setdefault(key, SerialExecutor())
                fut = sex.submit(call)
                return fut.result(timeout=pol.timeout) if pol.timeout else fut.result()
            fut = self._tpool.submit(call)
            return fut.result(timeout=pol.timeout) if pol.timeout else fut.result()

        return call()

    def handle_future_obj(self, cmd: Any) -> Future:
        """非阻塞（dataclass 命令兼容）。"""
        spec = self._resolve_obj(cmd)
        if spec is None:
            raise KeyError(f"No handler for {type(cmd).__name__}")
        kind, (fn, pol) = spec
        key = pol.exclusive_key(cmd) if callable(pol.exclusive_key) else None

        if kind == "process":
            submit = lambda: self._ppool.submit(fn, cmd)
            if pol.ordered and key:
                sex = self._serial_execs.setdefault(key or "", SerialExecutor())
                return sex.submit(lambda: submit().result(pol.timeout))
            return submit()

        def call():
            if key:
                with self._lock:
                    lk = self._key_locks.setdefault(key, threading.Lock())
                with lk:
                    return fn(cmd)
            return fn(cmd)

        if kind == "thread":
            if pol.ordered and key:
                sex = self._serial_execs.setdefault(key, SerialExecutor())
                return sex.submit(call)
            return self._tpool.submit(call)

        return self._tpool.submit(call)  # inline -> 包装

    # ---------- 解析 ----------
    def _resolve_named(self, name: str):
        with self._lock:
            if name in self._named_process:
                return ("process", self._named_process[name])
            if name in self._named_handlers:
                fn, pol = self._named_handlers[name]
                kind = pol.executor if pol.executor in ("inline", "thread", "process") else "inline"
                return (kind, (fn, pol))
        return None

    def _resolve_obj(self, cmd: Any):
        t = type(cmd)
        with self._lock:
            if t in self._process_dc:
                return ("process", self._process_dc[t])
            if t in self._handlers_dc:
                fn, pol = self._handlers_dc[t]
                kind = pol.executor if pol.executor in ("inline", "thread", "process") else "inline"
                return (kind, (fn, pol))
        return None

    def shutdown(self, wait: bool = True) -> None:
        self._tpool.shutdown(wait=wait, cancel_futures=False)
        self._ppool.shutdown(wait=wait, cancel_futures=False)

# =============================
# Demo
# =============================
if __name__ == "__main__":
    bus = CommandBus()

    # ===== 命名命令（推荐）=====
    @CommandBus.handler("save_to_disk",
                        executor="thread",
                        key=lambda kw: kw["path"],  # 同一路径互斥
                        ordered=True)               # 严格 FIFO
    def save_to_disk(*, path: str, text: str) -> str:
        time.sleep(0.02)
        with open(path, "a", encoding="utf-8") as f:
            f.write(text + "\n")
        return "ok"

    # CPU 密集：进程池（顶层函数）
    def count_primes(*, n: int) -> int:
        def is_p(x: int) -> bool:
            if x < 2: return False
            if x % 2 == 0: return x == 2
            i, r = 3, int(x**0.5)
            while i <= r:
                if x % i == 0: return False
                i += 2
            return True
        return sum(1 for i in range(n + 1) if is_p(i))

    @CommandBus.process_task("count_primes", task_fn=count_primes, timeout=10.0)
    def _dummy(): pass

    # =====（可选）兼容 dataclass 的旧接口 =====
    # from dataclasses import dataclass
    # @dataclass
    # class AppendOrdered: path: str; text: str
    # @CommandBus.handler_dc(AppendOrdered,
    #     policy=ExecPolicy(executor="thread", exclusive_key=lambda c: c.path, ordered=True))
    # def handle_append_ordered(cmd: AppendOrdered) -> str:
    #     with open(cmd.path, "a", encoding="utf-8") as f:
    #         f.write(cmd.text + "\n")
    #     return "ok"

    # ===== 调用演示（命名）=====
    log = "demo.log"
    if os.path.exists(log): os.remove(log)
    f1 = bus.handle_future("save_to_disk", path=log, text="hello")
    f2 = bus.handle_future("save_to_disk", path=log, text="world")
    print("save:", f1.result(), f2.result())
    print("file:", open(log, "r", encoding="utf-8").read().strip().splitlines())

    print("primes <=", bus.handle("count_primes", n=200_000))

    bus.shutdown()