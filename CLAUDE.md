# CLAUDE.md — codechu-log

Bootstrap per `codechu-org/ai/AGENTS.md` §0 before any work. Prefer
the local clone at `$org_home/codechu-org/ai/AGENTS.md` (if
`~/.config/codechu/config.toml` has `org_home` set); otherwise
WebFetch the public raw URL
<https://raw.githubusercontent.com/codechu/codechu-org/main/ai/AGENTS.md>.
This file lists only product-local overrides.

## Product-local notes

- Pure stdlib structured logging. **No** external runtime
  dependencies. `codechu-term` is an optional console-detection hint;
  the library degrades gracefully to `sys.stderr.isatty()`.
- Public API: `setup`, `Context`, `bind`, `structured`,
  `StructuredLogger`. Anything starting with `_` is internal.
- JSON line schema (`docs/API.md`) is part of the public contract.
  Renaming or removing a field is a breaking change.
- `Context` must remain `contextvars`-backed (not `threading.local`)
  so async propagation keeps working.
- Coverage target: ≥85 %.

## Discipline reminders (org rules apply)

- Conventional Commits, no AI signature.
- No `--no-verify`, no force push, no unapproved publish.
- See `codechu-org/ai/AGENTS.md` for the full list.
