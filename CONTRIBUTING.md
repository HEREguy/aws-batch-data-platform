# Contributing to aws-batch-data-platform

Thank you for contributing! This project is a batch ELT platform (Airflow + S3 + Glue + Athena + dbt) built as a portfolio-quality data engineering project. Please read this guide before submitting changes.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Getting Started](#getting-started)
3. [Coding Standards](#coding-standards)
4. [Available AI Skills](#available-ai-skills)
5. [Review & Pull Request Process](#review--pull-request-process)
6. [Testing](#testing)
7. [Diagrams](#diagrams)
8. [Release & UAT Gates](#release--uat-gates)

## Project Overview

**aws-batch-data-platform** builds a reproducible batch ELT pipeline:
- Extracts data from a public API/dataset
- Writes partitioned Parquet to Amazon S3
- Registers tables in the AWS Glue Data Catalog
- Queries/transforms with Athena and dbt
- Orchestrates with Airflow running locally via Docker Compose
- Dependency management with `uv`

The project lives under `airflow-elt-project/`. Full plans are in `docs/PROJECT_PLAN.md`.

## Getting Started

### Prerequisites

- Python 3.11 or 3.12
- [`uv`](https://docs.astral.sh/uv/) (dependency manager)
- Docker & Docker Compose (for local Airflow)
- An AWS account (for actual deployment; local development uses mocked services in tests)

### Setup

```bash
# From the repo root
cd airflow-elt-project

# Create virtual environment and install dependencies
uv sync --dev

# Run the test suite
uv run pytest

# Run linting
uv run ruff check .

# Run type checking
uv run mypy
```

### Pre-commit

The project uses `pre-commit` (configured in `pyproject.toml` dev dependencies). Install and activate it:

```bash
uv run pre-commit install
```

## Coding Standards

All Python code must follow the standards defined in the **python-programmer** skill (`.copilot/skills/python-programmer/SKILL.md`). Key points:

| Standard | Requirement |
|----------|-------------|
| Python version | 3.12+ compatibility (project range `>=3.11,<3.13`) |
| Style | PEP 8, enforced by `ruff` (line-length 100) |
| Type hints | All signatures annotated; use `X | None`; built-in generics (`list[str]`) |
| Paths | `pathlib.Path()` everywhere; `Path.resolve()` when comparing as strings |
| String formatting | f-strings only |
| Docstrings | Google style; no module-level docstrings for internal files unless complex |
| Imports | Module level only; stdlib → third-party → local |
| Error handling | Fail fast, clear errors, custom exception classes, `raise ... from`; no bare `except:` |
| Configuration | No hardcoded policy values; expose as parameters/CLI options |
| Tests | `pytest`; functional test file names (no `test_phase2_cli.py` style) |

Before marking a task complete, run the **Robustness Checklist** from the python-programmer skill:
- All external dependencies and preconditions identified and validated?
- No silent failures — add explicit error signaling/logging?
- Policy/config values not hardcoded where parameters are appropriate?
- Subprocess/network/file operations bounded by timeouts?
- Tests cover happy path, error paths, and key edge cases?

## Available AI Skills

This repository includes three AI assistant skills under `.copilot/skills/`. When working with an AI assistant, explicitly invoke the skill by name so the correct system prompt is loaded.

| Skill | Path | When to use |
|-------|------|-------------|
| **python-programmer** | `.copilot/skills/python-programmer/SKILL.md` | Writing/refactoring Python, CLI tools, test configuration |
| **python-grumpy-reviewer** | `.copilot/skills/python-grumpy-reviewer/SKILL.md` | Code review, PR review, test audits, UAT readiness |
| **drawio-diagram** | `.copilot/skills/drawio-diagram/SKILL.md` | draw.io architecture/data-flow/infrastructure diagrams |

### Example invocations

- "Use the **python-programmer** skill to add a new Airflow task to `elt_pipeline.py` following project standards."
- "Use the **python-grumpy-reviewer** skill to review my changes before I open the PR."
- "Use the **drawio-diagram** skill to create an architecture diagram for the new S3 → Glue → Athena flow."

See `AGENTS.md` for the full skill reference and invocation examples.

## Review & Pull Request Process

1. **Fork** the repository and create a feature branch from `main`.
2. **Implement** your changes following the coding standards above.
3. **Self-review**: run `ruff check`, `mypy`, and `pytest` locally.
4. **Invoke `python-grumpy-reviewer`** on your changes (see Available AI Skills) before requesting review. Apply findings and re-review once if needed (max 2 review cycles).
5. **Open a PR** against `main`. Include:
   - A clear description of what changed and why
   - Links to any related issues
   - Screenshots or diagram updates if the change affects architecture
   - Test results / coverage output
6. **CI** runs tests, lint, and Terraform validation on every PR.
7. **Maintainer review** — at least one approval required before merge.

### When `python-grumpy-reviewer` is required

Run it for any of these change profiles (from the skill's Automated Feedback Loop):

| Change profile | Action |
|----------------|--------|
| Docs/comments/format-only | Fast self-check only |
| Small code tweak, no boundary changes | Fast self-check; optional grumpy review |
| Logic change or test change | Fast self-check + grumpy review |
| Boundary change (I/O, DB, subprocess, auth, serialization) | Fast self-check + grumpy review (required) |
| Large refactor or multi-file behavior change | Fast self-check + grumpy review + one re-review |
| PR-ready or release-candidate | Full grumpy review with UAT gate output |

Skip grumpy review only when the change is docs/format-only or a trivial rename with no behavior change and a clean fast self-check.

## Testing

- Test framework: `pytest` with `pytest-cov` and `pytest-mock`
- AWS mocking: `moto` for unit tests (S3, Glue, Athena, etc.)
- Test paths: `tests/unit/` and `tests/integration/`
- Test file naming: functional names describing **what** is tested (e.g., `test_cli_add_command.py`), never temporal/version markers (`test_phase2_cli.py`, `test_v2_validators.py`)
- Coverage target: ≥80% for business logic
- Every test must have at least one meaningful assertion; no `assert mock.called`-style tests; no `time.sleep()` in tests
- Each external dependency interaction needs at least one failure-mode test

Run tests:

```bash
uv run pytest
uv run pytest --cov --cov-report=html
```

## Diagrams

All technical diagrams (architecture, data flow, infrastructure, swimlanes) must be created as draw.io `.drawio` XML files using the **drawio-diagram** skill.

- File naming: `descriptive_name.drawio` (underscores, no spaces)
- Store diagrams under `docs/` (e.g., `docs/architecture.drawio`, `docs/deployment.drawio`)
- Connections must be minimal (`source`/`target` only) for auto-adjusting behavior
- Grid: 10px; canvas standard `1600×1200`; text color `#333333`
- Validate by opening in draw.io desktop or web app

Do not use Mermaid or markdown tables for technical architecture diagrams.

## Release & UAT Gates

Before a PR is considered release-ready or handed off to UAT, a full **python-grumpy-reviewer** UAT review is required. The reviewer must produce:

1. **Findings** grouped by section (Design, Code Quality, Types, Tests, Security, Performance) with severity levels (BLOCKER/MAJOR/MINOR/NIT)
2. **UAT Evidence** — Hard Gates (PASS/FAIL/UNKNOWN), Confidence Checks (PASS/FAIL/UNKNOWN), Residual Risks
3. **Greatest Risk Areas** (top 3, prioritized by blast radius × likelihood)
4. **UAT Decision**: one of
   - **Not Ready for UAT** — any hard gate fails or critical evidence is missing
   - **Ready for UAT with Exceptions** — no blockers, documented residual risk accepted
   - **Ready for UAT** — all hard gates and confidence checks pass, no unresolved high-risk ambiguity

If any required evidence is missing, mark it "Unknown" and downgrade the UAT decision accordingly. Do not guess.
