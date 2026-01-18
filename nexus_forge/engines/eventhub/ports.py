from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from uuid import UUID

from nexus_forge.contracts.events import EventEnvelopeV01


class Port(ABC):
    @abstractmethod
    def publish(self, event: EventEnvelopeV01) -> None: ...

    @abstractmethod
    def subscribe(
        self, event_type: str, handler: Callable[[EventEnvelopeV01], None]
    ) -> None: ...

    @abstractmethod
    def read_all(self) -> Sequence[EventEnvelopeV01]: ...

    @abstractmethod
    def read_by_correlation_id(
        self, correlation_id: UUID
    ) -> Sequence[EventEnvelopeV01]: ...
