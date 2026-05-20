# Contributing to codechu-log

Thanks for thinking about contributing. `codechu-log` is a small
stdlib-only structured logging library. Patches that stay focused,
well-tested, and dependency-free are warmly received.

## Development setup

```bash
git clone https://github.com/codechu/log-py.git
cd log-py
pip install -e ".[dev]"
pytest -q
ruff check src tests
```

## Workflow

- Branch names: `feature/<short>`, `fix/<short>`, `refactor/<short>`,
  `docs/<short>`, `test/<short>`.
- Commit messages: [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`).
- Open a PR using the template; describe the *why* in the body.
- One change per PR — keep diffs reviewable.

## Tests

- `pytest -q` must pass; coverage stays at **≥85 %**.
- New feature → new test. Cover the edge cases: nested `Context`,
  async propagation, rotation thresholds, redaction across both
  formatters.

## Public API discipline

The public surface is `setup`, `Context`, `bind`, `structured`, and
`StructuredLogger`. The JSON-line schema is part of the contract —
renaming or removing a field is a breaking change and ships in a major
version bump.

No external runtime dependencies. `codechu-term` is an optional hint
only; the library must work with stdlib alone.

## Style

- `ruff check` + `ruff format` clean.
- Type hints on public APIs (`from __future__ import annotations`).

## Security

If you find a security issue, see [SECURITY.md](SECURITY.md) — do not
open a public issue for it.
