from abc import ABC, abstractmethod
from collections.abc import MutableMapping

from nexus_forge.contracts.events import EventEnvelopeV01
from nexus_forge.contracts.workflows import WorkflowSpec
from nexus_forge.engines.eventhub.in_memory import InMemoryEventHub
from nexus_forge.engines.pluginkit.registry import DemoRegistry
from nexus_forge.engines.policyengine.simple_allowlist import DemoPolicyEngine


class FlowForgeRuntime(ABC):
    @abstractmethod
    def register_workflow(self, spec: WorkflowSpec) -> None: ...

    @abstractmethod
    def on_event(self, event: EventEnvelopeV01) -> None: ...


class DemoFlowForgeRuntime(FlowForgeRuntime):
    def __init__(
        self,
        event_hub: InMemoryEventHub,
        policy_engine: DemoPolicyEngine,
        plugin_registry: DemoRegistry,
    ) -> None:
        self._workflows_by_triggers: MutableMapping[str, WorkflowSpec] = dict()
        self.event_hub = event_hub
        self.policy_engine = policy_engine
        self.plugin_registry = plugin_registry

    def register_workflow(self, spec: WorkflowSpec) -> None:
        self._workflows_by_triggers[spec.trigger] = spec

    def on_event(self, event: EventEnvelopeV01) -> None:
        if event.type_ in self._workflows_by_triggers:
            workflows_by_triggers: WorkflowSpec = self._workflows_by_triggers[
                event.type_
            ]
            for step in workflows_by_triggers.steps:
                print(f"Doing step, name: {step.name}, action: {step.action}")
