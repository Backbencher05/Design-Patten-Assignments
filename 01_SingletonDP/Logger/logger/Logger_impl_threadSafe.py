from datetime import datetime
from threading import Lock

from .logger import Logger, LogLevel


class LoggerImpl(Logger):

    _instance = None
    _lock = Lock()

    def __init__(self):
        self.log_file_path = None
        self.file_writer = None

    @staticmethod
    def get_instance() -> Logger:
        with LoggerImpl._lock:
            if LoggerImpl._instance is None:
                LoggerImpl._instance = LoggerImpl()

        return LoggerImpl._instance

    @staticmethod
    def reset_instance() -> None:
        with LoggerImpl._lock:
            if LoggerImpl._instance is not None:
                LoggerImpl._instance.close()

            LoggerImpl._instance = None

    def set_log_file(self, file_path: str) -> None:
        with LoggerImpl._lock:
            if self.file_writer is not None:
                self.file_writer.close()

            self.log_file_path = file_path
            self.file_writer = open(file_path, "a", encoding="utf-8")

    def get_log_file(self) -> str:
        return self.log_file_path

    def log(self, level: LogLevel, message: str) -> None:
        with LoggerImpl._lock:
            if self.file_writer is None:
                raise Exception("Logger is not initialized")

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = (
                f"{timestamp} [{level.name}] {message}\n"
            )

            self.file_writer.write(log_message)

    def flush(self) -> None:
        with LoggerImpl._lock:
            if self.file_writer is not None:
                self.file_writer.flush()

    def close(self) -> None:
        with LoggerImpl._lock:
            if self.file_writer is not None:
                self.file_writer.close()
                self.file_writer = None