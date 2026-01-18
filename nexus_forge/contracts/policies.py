from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum as PyEnum
from typing import Any
from uuid import UUID


class PolicyDecisionEnum(PyEnum):
    allow = "allow"
    deny = "deny"


@dataclass(frozen=True, kw_only=True)
class PolicyInput:
    id: UUID
    name: str
    context: str
    action: str
    resource: str
    actor: str | None = field(default=None)


@dataclass(frozen=True, kw_only=True)
class PolicyDecision:
    id: UUID
    policy_id: UUID
    policy_name: str
    decision: PolicyDecisionEnum
    reason: str
    trace: list[Mapping[str, Any]]
    policy_version: int
    class_up: int
