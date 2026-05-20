# Changelog

[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) + [SemVer](https://semver.org/).

## [Unreleased]

## [0.1.0] — 2026-05-20

### Added
- `setup(name, *, level, file, json, max_bytes, backup_count, fmt, redact)`
  — one-call logger configuration with `RotatingFileHandler` and a
  TTY-aware console handler (uses `codechu-term.is_tty` if installed,
  else `sys.stderr.isatty`).
- `Context(**fields)` — context manager backed by `contextvars`. Nested
  scopes merge, child wins on key conflict, propagation survives
  `await` and `asyncio.Task` boundaries.
- `bind(logger, **fields)` and `structured(logger)` — return a
  `StructuredLogger` that lifts call-site kwargs into the structured
  payload of every record.
- JSON formatter emitting one object per line: `ts` (ISO-8601 UTC),
  `level`, `logger`, `msg`, `fields`, `exc_info`, `pid`, `thread`.
- Redaction via `setup(..., redact=[...])` — replaces listed keys with
  `<redacted>` in both text and JSON output.
