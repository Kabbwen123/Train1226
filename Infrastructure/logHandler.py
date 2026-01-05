import os
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from typing import Any

class Logger:
    def __init__(
        self,
        log_dir: str = "log",
        enable_file: bool = True,
        log_level: int = logging.INFO,
        file_log_level: int = logging.INFO,
        console_log_level: int = logging.INFO,
    ):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.logger.propagate = False  # 防止重复输出

        # 记录启动时间，供其他组件使用同一时间戳
        self.start_time = datetime.datetime.now()
        self.log_root = log_dir

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 控制台日志处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_log_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 文件日志处理器
        self.date_dir = os.path.join(log_dir, self.start_time.strftime("%Y-%m-%d"))
        if enable_file:
            os.makedirs(self.date_dir, exist_ok=True)
            log_filename = os.path.join(
                self.date_dir,
                self.start_time.strftime("%Y-%m-%d-%H-%M-%S.log")
            )
            file_handler = TimedRotatingFileHandler(
                log_filename, when="midnight", backupCount=7, encoding="utf-8"
            )
            file_handler.setLevel(file_log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.logger, name)
