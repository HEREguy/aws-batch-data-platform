---
name: python-programmer
description: 'Python development standards and best practices. Use when writing, reviewing, or scaffolding Python projects: PEP 8, type hints, Click CLI, pytest, uv, pyproject.toml, pathlib, docstrings, packaging, cross-platform compatibility, error handling, imports, dependencies, precondition validation, parameterized configuration, and error-path testing.'
argument-hint: 'Describe the Python task or project to work on'
---

# Python Programmer

## When to Use

- Writing new Python modules, scripts, or packages
- Reviewing or refactoring existing Python code for standards compliance
- Creating CLI tools with Click and rich-click
- Setting up or fixing test configurations

> To bootstrap a new project from templates, use the `new-python-project` skill instead.

## Standards

### Language & Compatibility
- Python 3.12+ compatibility required
- PEP 8 code style
- Cross-platform compatibility (Windows, Linux, macOS)
- No encoding declarations (PEP 3120 — UTF-8 is the default)

### Docstrings & Comments
- Google style docstrings
- No module-level docstrings for internal files; only add them when complex situations genuinely need explanation
- Do not annotate comments with recency markers (e.g., avoid `# NEW:`, `# Updated:`)

### Imports
- All imports at module level (top of file), never inside functions or methods
- Follows PEP 8 import ordering: stdlib → third-party → local

### Type Hints
- Always annotate function and method signatures (parameters and return types)
- Use `X | None` instead of `Optional[X]` (Python 3.10+ union syntax)
- Use `from __future__ import annotations` for forward references when needed
- Use built-in generics (`list[str]`, `dict[str, int]`) rather than `typing.List`, `typing.Dict`

### Paths
- Always use `pathlib.Path()` when constructing complete or partial file system paths
- When comparing filesystem paths as strings, always normalize them first using `Path.resolve()` and convert to string. Account for Windows case-insensitivity and relative path variations.

### String Formatting
- Use f-strings for all string interpolation; avoid `.format()` and `%` formatting

### Error Handling
- Comprehensive error handling at system boundaries
- Validate preconditions explicitly before performing work (required tools installed, required files exist, required config present)
- Fail fast with clear, actionable errors; never fail silently or return `None` for a failed operation unless `None` is an explicit, documented result
- For subprocess and external operations, set explicit timeouts and handle timeout failures clearly
- Do not add error handling for scenarios that cannot occur
- Define custom exception classes for domain-specific errors rather than raising generic `Exception`
- Always re-raise with context: `raise NewError("msg") from original_exc`
- Never use bare `except:` — always specify the exception type
- Silent fallbacks as code smells: Be suspicious of code like `if condition: do_A() else: do_B()` where B is a fallback that hides errors. Document whether the fallback is intentional or masking a bug. Prefer explicit validation and clear errors.

### Configuration & Parameterization
- Do not hardcode policy/configuration values inside function bodies when they may vary by environment or user needs
- Expose namespace-like values, limits, thresholds, schema versions, output paths, and similar policy decisions as parameters or CLI options
- Keep sensible defaults, but make overrides explicit and documented
- If a value is intentionally fixed, document why it is fixed

### Resource Management
- Always use context managers (`with` statements) for file I/O, network connections, and any resource that requires cleanup
- When performing I/O with side effects (filesystem, network, database), order operations so state is mutated AFTER the operation succeeds, not before. Add rollback comments if state cannot be undone.

### Public API
- Define `__all__` in public-facing modules to explicitly declare the exported interface

## Packaging & Tooling

### pyproject.toml
- Modern Python packaging with `uv`
- Each dependency listed on a separate line for readability
- Include `[dependency-groups]` for `dev` and `docs` groups
- Add runtime dependencies under `[project] dependencies`; add dev/test tools under `[dependency-groups] dev`; add MkDocs and plugins under `[dependency-groups] docs`

### Running Python
- Use `uv run python` when invoking Python from the command line to ensure the correct virtual environment is used

### Pytest
- When invoking pytest programmatically, use `pytest.main(args)` instead of subprocess calls

### Package Version
- Expose `__version__` via `importlib.metadata.version()` so the installed package version is always the source of truth

## CLI (Click / rich-click)

- Use `rich_click` (`import rich_click as click`) for all CLI entry points — it provides rich formatting with no API changes
- Enable markup and markdown at module level:
  ```python
  click.rich_click.USE_RICH_MARKUP = True
  click.rich_click.USE_MARKDOWN = True
  ```
- The entry point function must be named `cli` (matching `pyproject.toml` `{{package_name}}.cli:cli`)
- Use `@click.version_option(version=package_version, prog_name=package_name)` to wire up `--version` from package metadata
- Initialize logging before the CLI group with `configure_logging()`; obtain a module-level logger with `logging.getLogger("{{package_name}}")`
- For options with default values, use `show_default=True` instead of embedding the default in the help string
- Do not use arguments.  Only use options (with `--option-name`) for CLI parameters, even if they are required.  This provides a more consistent user experience and allows for better help text formatting.
- For required options, use `required=True` and avoid embedding "required" in the help string since Click will automatically indicate that the option is required in the help output.
- Use `no_args_is_help=True` on the Click group to automatically show help when no arguments are provided, improving usability.  Also apply this to subcommands where it makes sense.
- DRY in CLI commands: CLI commands often have repeated boilerplate (argument parsing, validation, error handling). Extract helper functions for common patterns (e.g., `_validate_skill_exists()`, `_normalize_path()`).

## Logging

- Use a dict-based logging config (`logging.config.dictConfig`) with separate formatters for human-readable and parsable output
- Use a `RotatingFileHandler` for file output (10 MB max, 5 backups)
- Call `configure_logging()` at the start of `cli.py` before the Click group is defined
- Obtain module-level loggers with `logging.getLogger("<package_name>")`

## Deployment
- Automated deployment and installation workflows preferred

## Markdown (in project docs)
- Always add a blank line before bullet lists that follow non-header text

## Test-first Development
Development follows a **test-first (TDD)** workflow: write failing tests that define the expected behavior, then write the minimum code to make them pass, then refactor. No production code is written without a corresponding failing test.

Before writing implementation code, define at least one failing test for:
- Happy path behavior
- At least one error path
- At least one relevant edge case/boundary condition

### Testing Standards
- Place shared fixtures and helpers in `conftest.py` at the appropriate directory level
- Use `@pytest.mark.parametrize` for testing multiple input/output combinations
- Mock external I/O (network, filesystem, subprocesses) at the boundary; do not mock internal implementation details
- Test one behavior per test function; use descriptive names (`test_<unit>_<scenario>_<expected>`)
- Prefer `pytest.raises` context manager for asserting exceptions
- Use `tmp_path` fixture for temporary file operations rather than creating files manually
- Add explicit tests for malformed/empty input, missing dependencies, timeout behavior, and other identified precondition failures
- Do not stop at "no exception raised" assertions; verify correctness of outputs, side effects, and error messages
- For each external dependency interaction, include at least one failure-mode test

### Test File Naming (Required)
- Test file names must describe **what** they test, not **when** they were written.
- Do not use temporal/status/version markers in test file names.

Avoid these anti-patterns:
- `test_phase2_cli.py`
- `test_sprint3_auth.py`
- `test_v2_validators.py`
- `test_experimental_foo.py`

Use functional names like:
- `test_cli_commands.py`
- `test_cli_add_command.py`
- `test_auth_validators.py`
- `test_user_registration_flow.py`

Decision rule for related command tests:
- Use one file per command when tests are mostly independent (`test_cli_add_command.py`, `test_cli_init_command.py`).
- Use one broader command file when fixtures are heavily shared (`test_cli_commands.py`).

Rationale:
- Test names are discoverable artifacts and should communicate intent.
- Temporal markers become stale and mislead future maintainers.
- Functional names improve pytest discovery and IDE navigation.
- Refactoring behavior-based names is easier than maintaining phase/version-based names.

## Robustness Checklist (Required)

Before finalizing code, perform this self-check:

- [ ] Have all external dependencies and preconditions been identified and validated?
- [ ] Can any step fail silently? If yes, add explicit error signaling/logging.
- [ ] Are policy/config values hardcoded where parameters/options are more appropriate?
- [ ] Are subprocess/network/file operations bounded by timeouts where relevant?
- [ ] Do tests cover happy path, error paths, and key edge cases?

## Automated Feedback Loop (Efficiency-First)

Use `python-grumpy-reviewer` as a targeted gate, not a default after every tiny change.

### Loop Stages

1. Fast self-check (always)
- Run linting, type checking, and focused tests first.
- Fix obvious failures before requesting a full review.

2. Conditional grumpy review (run only when triggered)
- Trigger when any of the following are true:
  - Production logic changed
  - Tests changed materially
  - System boundary code changed (filesystem, network, DB, subprocess, serialization, auth)
  - Refactor is non-trivial (multi-file, structural, or behavior-affecting)
  - Diff size is large enough to hide subtle regressions

- Skip grumpy review when all are true:
  - Change is docs/comments/format-only, or a trivial rename
  - No behavior change
  - Fast self-check is clean

3. Repair pass and bounded re-review
- Apply fixes for findings.
- Run one re-review pass to verify closure.
- Maximum 2 review cycles per change set to avoid churn.

4. UAT gate at milestone boundaries
- Run full UAT-readiness review for PR-ready, release-candidate, or handoff-to-UAT milestones.
- Do not run full UAT gate after every incremental edit.

### Decision Table

| Change profile | Action |
|---|---|
| Docs/comments/format-only | Fast self-check only |
| Small code tweak, no boundary changes | Fast self-check; optional grumpy review |
| Logic change or test change | Fast self-check + grumpy review |
| Boundary change (I/O, DB, subprocess, auth, serialization) | Fast self-check + grumpy review (required) |
| Large refactor or multi-file behavior change | Fast self-check + grumpy review + one re-review |
| PR-ready or release-candidate | Full grumpy review with UAT gate output |