# Event Envelope — v0.1

## Purpose

The **Event Envelope** is the canonical container for every fact that flows through NexusForge.

An event represents **something that already happened**.  
It is not a command, not an instruction, and not an intention.

All engines, realms, workflows, policies, and plugins communicate **only** using events wrapped in this envelope.

This contract is foundational for:
- determinism and replay
- observability and auditability
- loose coupling between modules
- long-term evolution of the platform

---

## Design Principles

The Event Envelope follows these principles:

1. **Immutability**  
   Once created, an event must never be modified.

2. **Explicit causality**  
   Every event can be traced to:
   - a correlation chain
   - an optional causation event

3. **Versioned schemas**  
   Event payloads evolve via explicit versioning.

4. **Replay safety**  
   Events must contain enough information to be replayed deterministically.

5. **Engine-agnostic**  
   No engine-specific assumptions are embedded in the envelope.

---

## Event Envelope Fields (v0.1)

### Required Fields

| Field | Type | Description |
|------|------|-------------|
| `id` | UUID | Unique identifier for this event |
| `type_` | str | Event type identifier (see naming rules) |
| `version` | int | Schema version for this event type (≥ 1) |
| `timestamp` | datetime | Time the event occurred (UTC, timezone-aware) |
| `tenant_id` | str | Tenant or namespace identifier (use `"local"` for now) |
| `correlation_id` | UUID | Groups events belonging to the same workflow or request |
| `payload` | Mapping[str, Any] | Event-specific data (JSON-serializable) |

### Optional Fields

| Field | Type | Description |
|------|------|-------------|
| `causation_id` | UUID \| None | ID of the event that directly caused this event |
| `metadata` | Mapping[str, Any] | Diagnostic or trace information (source, actor, etc.) |

---

## Invariants (Must Hold)

The following invariants define correctness for Event Envelope v0.1:

1. `version` **must be ≥ 1**
2. `timestamp` **must be timezone-aware** and represent UTC time
3. `type_` **must be lowercase and dot-separated**
4. `correlation_id` **is always required**
5. `causation_id`, if present, **must reference a prior event**
6. `payload` **must be JSON-serializable**
7. Events are **immutable after creation**

Violating these invariants is considered a contract breach.

---

## Event Type Naming Convention

Event types follow this convention:
Examples:
- `system.started`
- `workflow.started`
- `workflow.completed`
- `policy.decided`
- `plugin.invoked`

Rules:
- lowercase only
- dot-separated
- describes a **fact in the past**
- avoid verbs implying intent (e.g., `request`, `ask`, `try`)

---

## Correlation vs Causation

### Correlation ID
- Groups related events across a workflow or request lifecycle
- Always present
- Typically generated at workflow start

### Causation ID
- Points to the **immediate parent event**
- Optional
- Enables precise event chains during replay and debugging

Example:
```bash
system.started (correlation_id = X)
└── workflow.started (causation_id = system.started)
└── policy.decided (causation_id = workflow.started)
```

---

## Versioning Strategy

- `version` refers to the **payload schema version** for a given event type
- Breaking changes require:
  - incrementing `version`
  - coexisting handlers (when replaying old events)

Envelope structure changes require a new **Event Envelope version**, which will be introduced via a new contract document.

---

## Non-Goals (v0.1)

The following are intentionally out of scope for v0.1:
- payload schema validation beyond basic invariants
- serialization format enforcement (JSON vs others)
- encryption or signing
- multi-tenant isolation logic

These will be addressed in later phases.

---

## Status

- **Version:** v0.1
- **Phase:** Platform Kernel
- **Stability:** Experimental but load-bearing