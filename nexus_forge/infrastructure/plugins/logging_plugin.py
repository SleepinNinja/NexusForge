from abc import ABC, abstractmethod
from typing import Any


class Logging(ABC):
    @abstractmethod
    def log_write_callable(self, **kwargs: Any) -> None: ...


class DemoLogging(Logging):
    def log_write_callable(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            print(f"key: {key}, value: {value}")
