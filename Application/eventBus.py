# eventbus.py
from __future__ import annotations
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, Future, wait, FIRST_EXCEPTION, ALL_COMPLETED
from typing import Any, Callable, Dict, List, Set, Optional, Tuple

Handler = Callable[..., Any]

class EventBus:
    """单总线场景：
    - @EventBus.on('topic') 类装饰器登记订阅（登记到类级表）
    - bus = EventBus(...) 实例化；用 bus.publish / bus.publish_async 发布
    - 无需 bind；发布时直接读取类级订阅表
    - 并行分发使用标准 ThreadPoolExecutor（无界队列：任务会排队）
    """

    # 类级：订阅登记表（装饰器写入）
    _class_lock = threading.RLock()
    _class_subs: Dict[str, Set[Handler]] = defaultdict(set)

    @classmethod
    def on(cls, topic: str):
        """类装饰器：@EventBus.on('topic')"""
        def deco(fn: Handler):
            with cls._class_lock:
                cls._class_subs[topic].add(fn)
            return fn
        return deco

    # 实例：发布与线程池
    def __init__(self, *, max_workers: Optional[int] = None, thread_name_prefix: str = "evt") -> None:
        """
        max_workers=None 使用库默认线程数（min(32, cpu+4)）。
        """
        self._pool = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix=thread_name_prefix)

    # —— 发布（实例方法）——
    def publish(self, topic: str, *args, **kwargs) -> None:
        """同步：在调用者线程中，顺序执行所有订阅者。"""
        with type(self)._class_lock:
            handlers = list(type(self)._class_subs.get(topic, ()))
        for h in handlers:
            try:
                h(*args, **kwargs)
            except Exception as e:
                # 生产中建议记录日志
                print(f"publish exception : {e}")
                raise

    def publish_async(self, topic: str, *args, **kwargs) -> List[Future]:
        """并行：每个订阅者一个任务，立即返回 futures（不会阻塞调用方）。"""
        with type(self)._class_lock:
            handlers = list(type(self)._class_subs.get(topic, ()))
        return [self._pool.submit(h, *args, **kwargs) for h in handlers]

    def publish_async_wait(
        self,
        topic: str,
        *args,
        timeout: Optional[float] = None,
        return_when: str = "FIRST_EXCEPTION",  # 或 "ALL_COMPLETED"
        **kwargs
    ) -> Tuple[Set[Future], Set[Future]]:
        """并行 + 等待（可超时），返回 (done, not_done)。"""
        futs = self.publish_async(topic, *args, **kwargs)
        mode = FIRST_EXCEPTION if return_when == "FIRST_EXCEPTION" else ALL_COMPLETED
        return wait(futs, timeout=timeout, return_when=mode)

    def shutdown(self, wait: bool = True) -> None:
        """优雅关闭线程池（应用退出时可调用）。"""
        self._pool.shutdown(wait=wait, cancel_futures=False)
