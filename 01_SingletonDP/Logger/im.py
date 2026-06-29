from __future__ import annotations
from threading import Lock
from datetime import datetime
from typing import Optional
from .logger import Logger, LogLevel


class LoggerImpl(Logger):
    _instance: Optional["LoggerImpl"] = None
    _lock = Lock()

    def __init__(self):
        # private fields
        self._file_path: Optional[str] = None
        self._file = None

    # -------------------------------
    #       SINGLETON METHODS
    # -------------------------------
    @staticmethod
    def get_instance() -> Logger:
        if LoggerImpl._instance is None:
            with LoggerImpl._lock:
                if LoggerImpl._instance is None:
                    LoggerImpl._instance = LoggerImpl()
        return LoggerImpl._instance

    @staticmethod
    def reset_instance() -> None:
        with LoggerImpl._lock:
            # Close existing instance before resetting
            if LoggerImpl._instance is not None:
                LoggerImpl._instance.close()

            LoggerImpl._instance = None

    # -------------------------------
    #       LOGGER METHODS
    # -------------------------------
    def set_log_file(self, file_path: str) -> None:
        # Close existing file if already opened
        if self._file:
            self._file.close()

        self._file_path = file_path
        self._file = open(self._file_path, "a", encoding="utf-8")

    def get_log_file(self) -> str:
        return self._file_path

    def log(self, level: LogLevel, message: str) -> None:
        if self._file is None:
            raise RuntimeError("Logger is not initialised. Call set_log_file() first.")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        formatted = f"{timestamp} [{level.name}] {message}\n"
        self._file.write(formatted)

    def flush(self) -> None:
        if self._file:
            self._file.flush()

    def close(self) -> None:
        if self._file:
            self._file.close()
            self._file = None
