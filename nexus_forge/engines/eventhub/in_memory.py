from collections.abc import Callable
from typing import Any

from nexus_forge.contracts.events import EventEnvelopeV01
from nexus_forge.engines.flowforge.runtime import DemoFlowForgeRuntime


class InMemoryEventHub:
    def __init__(self) -> None:
        self.event_list: list[EventEnvelopeV01] = []
        self.subscribers: dict[
            str, list[Callable[[DemoFlowForgeRuntime, EventEnvelopeV01], None]]
        ] = dict()

    def add_subscriber(self, event_type: str, handler: Any) -> None:
        self.subscribers[event_type].append(handler)

    def publish(self, event: EventEnvelopeV01) -> None:
        self.event_list.append(event)
        event_subscribers_callables: list[
            Callable[[DemoFlowForgeRuntime, EventEnvelopeV01], None]
        ] = self.subscribers[event.type_]

        for callable in event_subscribers_callables:
            # note: the self parameter is already bound to the callable.
            callable(event)  # type: ignore
