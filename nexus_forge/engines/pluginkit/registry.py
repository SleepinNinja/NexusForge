from abc import ABC, abstractmethod
from collections.abc import Callable, MutableMapping
from typing import Any


class Registry(ABC):
    @abstractmethod
    def register_capability(
        self, capability: str, callable_function: Callable[..., Any]
    ) -> None: ...

    @abstractmethod
    def invoke_capability(self, capability: str, **kwargs: Any) -> None: ...


class DemoRegistry(Registry):
    def __init__(self) -> None:
        self.registry: MutableMapping[str, Callable[..., Any]] = dict()

    def register_capability(
        self, capability: str, callable_function: Callable[..., Any]
    ) -> None:
        self.registry[capability] = callable_function

    def invoke_capability(self, capability: str, **kwargs: Any) -> None:
        if capability not in self.registry:
            raise Exception(
                f"Capability: {capability} is not present in registry, please register it first"
            )

        invocation_function: Callable[..., Any] = self.registry[capability]
        invocation_function(**kwargs)
