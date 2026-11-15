# Review Checklists

## Design & Architecture

- [ ] Does the module/class/function have a single, clear responsibility?
- [ ] Is there any abstraction with only one use case? (Delete it)
- [ ] Is anything reimplementing something already in the stdlib or a standard package?
- [ ] Are there mutable default arguments (`def f(x=[])`)?
- [ ] Is `None` being returned silently where an exception should be raised?
- [ ] Is exception handling used for control flow instead of conditions?
- [ ] Are there circular dependencies between modules?
- [ ] Do any classes exist purely to hold static methods? (Use a module)
- [ ] Is inheritance being used where composition would be simpler?
- [ ] Are there any data classes that should be `@dataclass` or `TypedDict` instead of a freeform dict?

## Code Quality

- [ ] Is naming consistent and descriptive throughout?
- [ ] Are there magic numbers or strings that need named constants?
- [ ] Is nesting deeper than 3 levels? (Early returns fix this)
- [ ] Are there bare `except:` or overly broad `except Exception:` blocks?
- [ ] Is there commented-out code? (Delete it — that's what git is for)
- [ ] Are there unused imports or variables?
- [ ] Are there `TODO` or `FIXME` comments older than a sprint?
- [ ] Is `global` or `nonlocal` used without good reason?
- [ ] Are there any `print()` statements left in non-CLI code?
- [ ] Are any functions longer than ~40 lines? (Probably doing too much)

## Types & Interfaces

- [ ] Do all public functions and methods have type hints?
- [ ] Is `Any` used where a real type could be specified?
- [ ] Are all return paths typed consistently (no implicit `None` returns on typed functions)?
- [ ] Do docstrings match the actual parameter/return types?
- [ ] Are `Optional[X]` and `X | None` used consistently (pick one)?
- [ ] Are there any mutable return values that callers might accidentally mutate?

## Test Quality

### Test Existence
- [ ] Are there tests at all?
- [ ] Is code coverage above an acceptable threshold (≥80% for business logic)?
- [ ] Are there tests for happy paths, sad paths, and edge cases?
- [ ] Are boundary values tested (0, -1, empty string, `None`, max values)?
- [ ] Are error paths and exceptions tested explicitly?

### Test Correctness
- [ ] Does every test have at least one meaningful assertion?
- [ ] Could any test pass even if the implementation is completely wrong?
- [ ] Is the test actually exercising the real code, or just a mock?
- [ ] Do tests depend on execution order? (They must not)
- [ ] Do tests depend on time, random values, or environment variables without seeding/mocking?
- [ ] Are there `time.sleep()` calls in tests? (Flakiness generator)

### Test Design
- [ ] Does each test test one thing?
- [ ] Is the test name a sentence that describes the scenario and expected outcome?
- [ ] Are fixtures reused appropriately, or is there test setup duplication?
- [ ] Are integration tests clearly separated from unit tests?
- [ ] Are there tests that assert the exact internal implementation (too brittle)?
- [ ] Are parametrized test cases used where the same logic is tested with many values?

### Common Useless Test Patterns (name them explicitly)
- `assert mock.called` — testing the mock, not the code
- `assert result is not None` — only valid if `None` is a documented error case
- Empty test body with only a `pass`
- Test that catches the exception it expects to be raised but doesn't `pytest.raises`
- Test with 10+ assertions that will fail on the first one with no context

## Security

*This is internal code. Focus on issues that cause real incidents, not public-API hardening.*

- [ ] Are there any hardcoded passwords, API keys, or tokens? (These end up in git)
- [ ] Is SQL built by string formatting instead of parameterized queries?
- [ ] Is `eval()` or `exec()` called on any variable input, even from internal sources?
- [ ] Is `pickle`, `yaml.load` (vs `yaml.safe_load`), or `shelve` used on data crossing service boundaries?
- [ ] Are credentials or secrets written to logs or stdout?
- [ ] Are subprocess calls using `shell=True` with any variable input?
- [ ] Are there any `os.chmod` calls setting world-writable permissions on shared systems?
- [ ] Are env-var-sourced secrets accessed without a clear error when the variable is missing?

**Skip unless there is a specific reason to flag:**
- Missing input validation on internal helper functions
- Lack of authentication/rate-limiting on internal tooling

## Performance

- [ ] Are there loops iterating over a list to find an item that should be a dict/set?
- [ ] Is an entire file or large dataset loaded into memory when streaming is possible?
- [ ] Are expensive operations (DB calls, API calls, file I/O) inside a loop that runs per-item?
- [ ] Are there repeated identical computations inside a loop (hoist them out)?
- [ ] Are generator expressions used where possible instead of building full lists?
