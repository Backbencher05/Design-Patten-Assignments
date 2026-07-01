from __future__ import annotations

from dataclasses import dataclass

from .builder import Builder


@dataclass
class DatabaseConfiguration:
    database_url: str
    username: str
    password: str
    max_connections: int
    enable_cache: bool
    is_read_only: bool

    @staticmethod
    def builder() -> DatabaseBuilder:
        return DatabaseConfiguration.DatabaseBuilder()

    class DatabaseBuilder(Builder["DatabaseConfiguration"]):

        def __init__(self):
            self._instance = DatabaseConfiguration(None, None, None, None, None, None)

        def build(self) -> DatabaseConfiguration:
            raise NotImplementedError("DatabaseBuilder.build")
