import uuid
from datetime import UTC, datetime

from nexus_forge.contracts.events import EventEnvelopeV01
from nexus_forge.contracts.workflows import StepSpec, WorkflowSpec
from nexus_forge.engines.eventhub.in_memory import InMemoryEventHub
from nexus_forge.engines.flowforge.runtime import DemoFlowForgeRuntime
from nexus_forge.engines.pluginkit.registry import DemoRegistry
from nexus_forge.engines.policyengine.simple_allowlist import DemoPolicyEngine
from nexus_forge.infrastructure.plugins.logging_plugin import DemoLogging

event_hub: InMemoryEventHub = InMemoryEventHub()
policy_engine: DemoPolicyEngine = DemoPolicyEngine()
plugin_registry: DemoRegistry = DemoRegistry()
logging_plugin: DemoLogging = DemoLogging()

flow_forge: DemoFlowForgeRuntime = DemoFlowForgeRuntime(
    event_hub=event_hub, plugin_registry=plugin_registry, policy_engine=policy_engine
)

plugin_registry.register_capability(
    capability="log.write", callable_function=logging_plugin.log_write_callable
)

startup_workflow: WorkflowSpec = WorkflowSpec(
    id=uuid.uuid4(),
    name="WorkflowSpec1",
    version=1,
    trigger="system.started",
    steps=[
        StepSpec(
            name="StepSpec1", action="log.write", inputs={"message": "System started"}
        )
    ],
)

flow_forge.register_workflow(spec=startup_workflow)
event_hub.add_subscriber(event_type="system.started", handler=flow_forge.on_event)

correlation_id: uuid.UUID = uuid.uuid4()
startup_event: EventEnvelopeV01 = EventEnvelopeV01(
    id=uuid.uuid4(),
    type_="system.started",
    correlation_id=correlation_id,
    timestamp=datetime.now(tz=UTC),
    version=1,
    tenant_id=str(uuid.uuid4()),
    payload={"some_key": "key_value"},
)


event_hub.publish(event=startup_event)
