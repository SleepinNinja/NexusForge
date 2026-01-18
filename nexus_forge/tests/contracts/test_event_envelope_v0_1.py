from datetime import UTC, datetime
from uuid import uuid4

import pytest
from contracts.events import EventEnvelopeV01


def _valid_event(**overrides):
    """Factory for a valid EventEnvelopeV01 with sane defaults."""
    base = dict(
        id=uuid4(),
        type_="system.started",
        version=1,
        timestamp=datetime.now(UTC),
        tenant_id="local",
        correlation_id=uuid4(),
        payload={"message": "hello"},
        causation_id=None,
        metadata={},
    )
    base.update(overrides)
    return EventEnvelopeV01(**base)


def test_constructs_with_required_fields():
    ev = _valid_event()
    assert ev.type_ == "system.started"
    assert ev.version == 1
    assert ev.tenant_id == "local"
    assert ev.payload["message"] == "hello"


def test_rejects_naive_timestamp():
    with pytest.raises(ValueError, match="not timezone aware"):
        _valid_event(timestamp=datetime.now())  # naive datetime


def test_accepts_timezone_aware_timestamp():
    # tz-aware non-UTC is still tz-aware; your current invariant accepts tz-aware.
    ist = UTC  # if you want a non-UTC example later, use zoneinfo
    ev = _valid_event(timestamp=datetime.now(ist))
    assert ev.timestamp.tzinfo is not None


@pytest.mark.parametrize(
    "bad_type",
    [
        "System.Started",  # uppercase not allowed
        "system..started",  # double dots not allowed
        ".system.started",  # leading dot not allowed
        "system.started.",  # trailing dot not allowed
        "system-started",  # dash not allowed by your regex
        "system.started1",  # digits not allowed by your regex
        "",  # empty not allowed
    ],
)
def test_rejects_invalid_type_patterns(bad_type: str):
    with pytest.raises(ValueError, match="Invalid type pattern"):
        _valid_event(type_=bad_type)


def test_rejects_version_zero():
    with pytest.raises(ValueError, match="Invalid version"):
        _valid_event(version=0)


def test_rejects_negative_version():
    with pytest.raises(ValueError, match="Invalid version"):
        _valid_event(version=-1)


def test_rejects_non_json_serializable_payload():
    with pytest.raises(ValueError, match="not JSON-serializable"):
        _valid_event(payload={"x": object()})  # object() cannot be JSON-dumped


def test_allows_json_serializable_payload():
    ev = _valid_event(
        payload={"a": 1, "b": True, "c": None, "d": ["x", 2], "e": {"k": "v"}}
    )
    assert ev.payload["e"]["k"] == "v"
