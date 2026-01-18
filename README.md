# NexusForge

NexusForge is a **product-grade, event-driven, policy-governed automation platform** built in Python.

It is designed as a learning and execution vehicle for building **deterministic, observable, and governable systems**, where AI assists decision-making but never executes side effects directly.

This repository starts as a **modular monolith** and evolves deliberately over time.

---

## What NexusForge *Is*

- A **platform**, not a single application
- **Contract-first**: events, workflows, and policies are explicit and versioned
- **Event-driven**: all behavior is triggered and explained via events
- **Policy-governed**: side effects are gated by explicit policy decisions
- **Deterministic and replayable**: executions can be reconstructed from logs and recorded I/O
- **Observable by default**: structured logs, correlation IDs, and audit trails are required

---

## What NexusForge Is *Not*

- ❌ Not a CRUD app
- ❌ Not a chatbot
- ❌ Not a collection of scripts
- ❌ Not microservices-first
- ❌ Not an AI agent that executes actions autonomously

AI in NexusForge **proposes and explains** — it never mutates state directly.

---

## Core Principles

- **Coherence over chaos**
  Clear module boundaries, explicit contracts, no hidden coupling.

- **Governance first**
  All side effects go through workflows, policies, and capability checks.

- **Determinism and replay**
  Every workflow run must be explainable and reproducible.

- **Observability by default**
  Logs, traces, and audit data are not optional.

- **Simplicity before scale**
  Start with a modular monolith; evolve only when justified.

---

## Repository Structure (High Level)
```bash
nexusforge/
├── engines/        # Core reusable engines (eventhub, flowforge, policyengine, pluginkit)
├── contracts/      # Canonical, versioned contracts (events, workflows, policies)
├── realms/         # Product domains built on top of engines
├── infrastructure/ # Logging, persistence, and runtime adapters
├── docs/           # ADRs, patterns atlas, and design documentation
├── tests/          # Unit, contract, and integration tests
```

Modules communicate **only via events or public interfaces** — never by importing internals of another module.

---

## Tooling & Quality Gates

- **Python:** 3.14
- **Package manager:** uv
- **Formatter:** black
- **Linter:** ruff
- **Type checker:** mypy
- **Test runner:** pytest
- **Pre-commit hooks:** required
- **CI:** mirrors local quality gates

A change is considered mergeable only if formatting, linting, type-checking, and tests pass locally and in CI.

---

## Current Status

**Phase 1: Platform Kernel**

- Repository structure established
- Bootstrap decisions recorded (ADR-000)
- Tooling and quality gates in place
- Canonical contracts (v0.1) next

No business logic, workflows, or AI components are implemented yet by design.

---

## License

TBD
