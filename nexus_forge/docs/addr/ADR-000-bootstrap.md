# ADR-000: Bootstrap Decisions

- **Status:** Accepted
- **Date:** 2026-01-17
- **Owners:** Project maintainers

## Context

NexusForge is a contract-first, event-driven platform. Early decisions must optimize for:
- coherence over chaos (clear boundaries + versioned contracts)
- determinism and replay (reproducible runs via event logs / recorded I/O)
- governance-first (policy gates for side effects)
- observability by default (structured logs + correlation IDs)
- simplicity before scale (modular monolith in Python)

This ADR records the initial project bootstrap choices so the codebase remains consistent and enforceable as it grows.

## Decision

### 1) Language Runtime

- **Python version:** **3.14**
- **Policy:** Pin the runtime version in repository tooling and CI.

**Notes / Risk:** Python 3.14 may be ahead of the ecosystem support curve (some dependencies may lag).
Mitigation:
- keep dependencies minimal in the kernel
- lock versions and maintain a fast downgrade path (e.g., to the latest stable Python) if a critical library blocks progress

### 2) Dependency & Environment Management

- **Package / env manager:** **uv**
- **Policy:** Use uv for:
  - virtual environment management
  - dependency resolution + locking
  - reproducible installs across machines and CI

Rationale: fast, modern workflow and strong reproducibility story—aligned with determinism goals.

### 3) Quality Gates / Tooling (Local + CI)

We enforce consistent code style and early defect detection from day one to prevent architectural drift and contract breakage.

- **Formatter:** `black`
  Rationale: eliminates subjective formatting; keeps diffs clean and reviewable.

- **Linter:** `ruff`
  Rationale: fast feedback on common errors and hygiene issues; helps prevent entropy in a modular monolith.

- **Type checker:** `mypy`
  Rationale: NexusForge is contract-driven (events, workflows, policies). Static typing reduces boundary bugs and supports determinism/replay by ensuring payload shapes and interfaces remain consistent.

- **Test runner:** `pytest`
  Rationale: supports unit + contract tests; enables safe refactors as engines evolve.

- **Pre-commit:** required
  Rationale: runs formatting/lint/type/tests before commits to block broken changes early.

- **CI:** mirrors pre-commit gates
  Rationale: consistent enforcement across all contributors and environments.

**Merge policy:** A change is mergeable only if formatting, linting, type-checking, and tests pass locally and in CI.

## Consequences

- We trade a slightly heavier initial setup for long-term velocity and reliability.
- Static typing + contract tests become primary tools for protecting engine boundaries.
- Any future change to core contracts must be versioned and accompanied by compatibility strategy and tests.
- If Python 3.14 ecosystem gaps block progress, we will revise this ADR with an explicit downgrade decision.

## Follow-ups

- Create `contracts/` module with v0.1 definitions:
  - Event Envelope
  - Workflow Spec
  - Policy Spec
- Establish pre-commit configuration to run: black, ruff, mypy, pytest
- Add CI workflow that runs the same checks on every push/PR
