import json
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from re import Match
from typing import Any
from uuid import UUID


@dataclass(frozen=True, kw_only=True)
class EventEnvelopeV01:
    id: UUID
    type_: str
    version: int
    timestamp: datetime
    tenant_id: str
    correlation_id: UUID
    payload: Mapping[str, Any]
    causation_id: UUID | None = field(default=None)
    metadata: dict[str, Any] = field(default_factory=lambda: {})

    def __post_init__(self) -> None:
        timestamp: datetime = self.timestamp
        is_timestamp_tz_aware: bool = (
            timestamp.tzinfo is not None and timestamp.utcoffset() is not None
        )

        if not is_timestamp_tz_aware:
            raise ValueError(f"timestamp {timestamp} is not timezone aware.")

        type_: str = self.type_
        has_only_lowercase_and_dot: Match[str] | None = re.fullmatch(
            pattern="^[a-z]+(\\.[a-z]+)*$", string=type_
        )
        if has_only_lowercase_and_dot is None:
            raise ValueError(f"Invalid type pattern: {type_}, dot-separated segments.")

        version: int = self.version
        if version < 1:
            raise ValueError(f"Invalid version {version}, must be greater than 0")

        """
        todo:
        add validation to causation_id to be present when event is a derived event.
        """

        payload: Mapping[str, Any] = self.payload
        try:
            json.dumps(obj=payload)
        except (OverflowError, TypeError) as e:
            raise ValueError(f"Payload is not JSON-serializable: {e}") from e
