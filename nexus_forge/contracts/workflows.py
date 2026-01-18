from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID


@dataclass(frozen=True, kw_only=True)
class StepSpec:
    name: str
    action: str
    inputs: Mapping[str, Any]
    retries: int = field(default=0)
    policy_gate: str | None = field(default=None)


@dataclass(frozen=True, kw_only=True)
class WorkflowSpec:
    id: UUID
    name: str
    version: int
    trigger: str
    steps: Sequence[StepSpec]

    def __post_init__(self) -> None:
        version: int = self.version
        if version < 1:
            raise ValueError(f"Invalid version {version}, must be greater than 0")
