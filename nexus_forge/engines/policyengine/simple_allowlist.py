import uuid
from abc import ABC, abstractmethod

from nexus_forge.contracts.policies import (
    PolicyDecision,
    PolicyDecisionEnum,
    PolicyInput,
)


class PolicyEngine(ABC):
    @abstractmethod
    def decide(self, input: PolicyInput) -> PolicyDecision: ...


class DemoPolicyEngine(PolicyEngine):
    def decide(self, input: PolicyInput) -> PolicyDecision:
        decision: PolicyDecisionEnum = PolicyDecisionEnum.deny

        if input.action == "log.write":
            decision = PolicyDecisionEnum.allow

        return PolicyDecision(
            id=uuid.uuid4(),
            policy_id=input.id,
            policy_name=input.name,
            decision=decision,
            reason="Valid policy action",
            trace=[{"trace_key1": 1, "trace_key2": 2}],
            policy_version=1,
        )
