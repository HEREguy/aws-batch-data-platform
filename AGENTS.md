# AGENTS.md — AI Assistant Guidance for aws-batch-data-platform

This file tells AI assistants how to work effectively in this repository. It documents the available skills, project conventions, and workflow gates.

## Repository Overview

**aws-batch-data-platform** — A reproducible batch ELT pipeline that downloads data from a public API/dataset, writes partitioned Parquet to Amazon S3, registers tables in the AWS Glue Data Catalog, and queries/transforms them with Athena and dbt. Airflow runs locally via Docker Compose. Python dependency management is via `uv`.

Key locations:
- `airflow-elt-project/` — The Python/Airflow project (DAGs, scripts, config, tests, Terraform)
- `airflow-elt-project/pyproject.toml` — Dependencies, ruff, mypy, pytest config
- `airflow-elt-project/dags/elt_pipeline.py` — The end-to-end batch pipeline
- `docs/PROJECT_PLAN.md` — Full project plan and architecture
- `.copilot/skills/` — Copilot skills (see below)

## Available Skills (`.copilot/skills/`)

Three skills are available. **Explicitly invoke the skill by name** when the situation matches — do not rely on auto-detection.

### 1. python-programmer

**Path:** `.copilot/skills/python-programmer/SKILL.md`

**When to use:** Writing new Python modules/scripts/packages, reviewing or refactoring existing Python for standards compliance, creating Click CLI tools, setting up or fixing test configuration.

**Key standards enforced:**
- Python 3.12+ compatibility (project requires `>=3.11,<3.13`; target 3.12+ where possible)
- PEP 8 code style, ruff with line-length 100
- Type hints on all function/method signatures; use `X | None` (not `Optional[X]`); built-in generics (`list[str]`, `dict[str, int]`)
- `pathlib.Path()` for all filesystem paths; normalize with `Path.resolve()` when comparing as strings
- f-strings for interpolation; no `.format()` or `%`
- Google-style docstrings; no module-level docstrings for internal files unless genuinely complex
- Imports at module level, ordered: stdlib → third-party → local
- Fail fast with clear errors; never silent `None` returns; custom exception classes; `raise ... from original_exc`
- No bare `except:`; explicit timeouts on subprocess/network/file ops
- Configuration values exposed as parameters/CLI options, not hardcoded
- Pytest with functional test file names (no temporal/version markers like `test_phase2_cli.py`)
- Robustness checklist required before finalizing code

**Invocation example:**
> "Use the **python-programmer** skill to refactor `elt_pipeline.py` so it follows project standards: pathlib, type hints, Google docstrings, and explicit precondition validation."

### 2. python-grumpy-reviewer

**Path:** `.copilot/skills/python-grumpy-reviewer/SKILL.md` (+ `references/checklist.md`)

**When to use:** Reviewing Python code, auditing test files, critiquing a design, "roasting" code before a real PR, checking UAT readiness. Triggers: *review, audit, critique, code review, PR review, "what's wrong with this code".*

**What it covers:** Design & architecture, code quality, types & interfaces, test quality, security (internal-code focus — hardcoded secrets, SQL injection via string formatting, `eval`/`exec`, `pickle`/`yaml.load`, `shell=True`, etc.), performance, UAT readiness gates.

**Severity levels:** BLOCKER / MAJOR / MINOR / NIT

**Output format:** Findings grouped by section with `Where`, `Problem`, `Fix`; required UAT Evidence section (Hard Gates, Confidence Checks, Residual Risks); Greatest Risk Areas; UAT Decision.

**Invocation example:**
> "Use the **python-grumpy-reviewer** skill to review `scripts/init_connections.py` and `dags/elt_pipeline.py` before I open the PR. Include UAT decision."

**Workflow integration (from python-programmer's Automated Feedback Loop):**
1. Fast self-check (always): linting (ruff), type checking (mypy), focused tests
2. Conditional grumpy review: run when production logic, tests, system-boundary code, or non-trivial refactors change; skip for docs/format-only or trivial renames with clean self-check
3. Repair pass + one bounded re-review (max 2 cycles)
4. Full UAT gate at PR-ready / release-candidate / handoff milestones

### 3. drawio-diagram

**Path:** `.copilot/skills/drawio-diagram/SKILL.md` (+ `references/templates.md`)

**When to use:** Creating professional draw.io (.drawio) XML diagrams — system architecture, data flow, technical tables/status matrices, flowcharts/swimlanes, timelines, infrastructure/network diagrams.

**Do NOT use for:** Simple markdown tables (use markdown), Mermaid-suitable diagrams (use mermaid in markdown), quick sketches (use draw.io UI directly).

**Key rules:**
- Base XML: `<mxfile host="app.diagrams.net" ...><diagram id="..." name="..."><mxGraphModel ...><root>...</root></mxGraphModel></diagram></mxfile>`
- Connections: minimal — just `source` and `target` with `<mxGeometry relative="1" as="geometry"/>` (auto-adjusts). Avoid `exitX/exitY/entryX/entryY`, fixed `mxPoint`, and `edgeStyle` unless specifically needed.
- Shapes: `vertex="1"`, `parent="1"`, unique descriptive IDs, explicit geometry (x, y, width, height)
- Grid: 10px; minimum gap 20–40px; standard canvas `pageWidth="1600" pageHeight="1200"`
- Colors: `#333333` text (not pure black), consistent palette, sufficient contrast
- Text: `&#xa;` for line breaks, `whiteSpace=wrap`, `html=1`
- File naming: `descriptive_name.drawio` (underscores, no spaces)
- Validate by opening in draw.io desktop or web app

**Invocation example:**
> "Use the **drawio-diagram** skill to create a data-flow diagram of the S3 → Glue → Athena pipeline and save it as `docs/architecture.drawio`."

## Project Conventions Summary

| Area | Convention | Source |
|------|-----------|--------|
| Python version | 3.11–3.12 (`pyproject.toml`: `>=3.11,<3.13`) | pyproject.toml |
| Dependency manager | `uv` | pyproject.toml |
| Linter | `ruff` (line-length 100, target py311) | pyproject.toml |
| Type checker | `mypy` | pyproject.toml |
| Test runner | `pytest` | pyproject.toml |
| CLI framework | Click / rich-click | python-programmer skill |
| Import order | stdlib → third-party → local | python-programmer skill |
| Type hint syntax | `X | None`, built-in generics | python-programmer skill |
| Path handling | `pathlib.Path`, `Path.resolve()` | python-programmer skill |
| Docstrings | Google style | python-programmer skill |
| Test naming | Functional names, no temporal markers | python-programmer skill |
| Diagram format | draw.io `.drawio` XML | drawio-diagram skill |

## Before You Finish Any Task

1. If you wrote or changed Python code, run ruff + mypy + pytest first (fast self-check).
2. If the change touched production logic, tests, or system-boundary code, invoke **python-grumpy-reviewer**.
3. If you created documentation with a technical diagram, invoke **drawio-diagram**.
4. Confirm new Python files follow **python-programmer** standards before considering the task done.

