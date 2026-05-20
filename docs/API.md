# codechu-log — API reference

Public surface (importable from `codechu_log`):

| Symbol | Kind | Purpose |
|---|---|---|
| `setup` | function | One-call logger configuration. |
| `Context` | context manager | Push structured fields into the current scope. |
| `bind` | function | Wrap a logger with always-on fields. |
| `structured` | function | Wrap a logger so call-site kwargs become fields. |
| `StructuredLogger` | class | Return type of `bind` / `structured`. |
| `__version__` | str | Library version string. |

## `setup(name, *, level="INFO", file=None, json=False, max_bytes=10*1024*1024, backup_count=5, fmt=None, redact=None)`

Returns a configured `logging.Logger`.

- `name` — logger name (typically dotted: `"myapp.api"`).
- `level` — standard `logging` level (`"INFO"`, `logging.DEBUG`, …).
- `file` — path to a rotating log file; omit for console-only.
- `json` — when `True`, every handler emits one JSON object per line.
- `max_bytes`, `backup_count` — forwarded to
  `logging.handlers.RotatingFileHandler`.
- `fmt` — custom text format string (ignored when `json=True`).
- `redact` — iterable of field keys to mask as `<redacted>`.

A console handler is attached when `stderr.isatty()`. If
`codechu-term` is installed its `is_tty()` is used instead.

`setup` is idempotent — calling it again with the same `name` removes
any previously attached handlers before adding new ones.

## `Context(**fields)`

Context manager that pushes `fields` into a `contextvars`-backed scope.
Nested contexts merge; child keys win on conflict. The scope propagates
across `await` and `asyncio.Task` boundaries.

```python
with Context(request_id="r1"):
    log.info("inside")        # fields = {"request_id": "r1"}
    with Context(user="onur"):
        log.info("nested")    # fields = {"request_id": "r1", "user": "onur"}
log.info("outside")           # fields = {}
```

## `bind(logger, **fields) -> StructuredLogger`

Return a wrapper that includes `fields` in every emitted record.

```python
log = bind(setup("api"), service="api")
log.info("ready")             # fields includes service=api
log.bind(request_id="r").info("hit")  # adds request_id
```

## `structured(logger) -> StructuredLogger`

Identical to `bind(logger)` — every call-site `**kwargs` becomes
structured fields.

```python
log = structured(setup("api"))
log.info("hello", user="onur", count=3)
```

## `StructuredLogger`

The return type of `bind` / `structured`. Exposes the standard logger
methods (`debug`, `info`, `warning`, `error`, `critical`, `exception`,
`log`) plus `.bind(**fields)` for further composition. The raw
`logging.Logger` is available as `.logger`.

Standard `logging` keyword arguments (`exc_info`, `stack_info`,
`stacklevel`, `extra`) are forwarded to the underlying logger; all
other kwargs are treated as structured fields.

## JSON output schema

Each JSON line is a single object with these keys:

| Key | Type | Notes |
|---|---|---|
| `ts` | string | ISO-8601 UTC, e.g. `2026-05-20T12:34:56.789012+00:00`. |
| `level` | string | `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL`. |
| `logger` | string | Logger name passed to `setup`. |
| `msg` | string | Result of `record.getMessage()` (after %-format). |
| `fields` | object | Merged structured fields. Order: `Context` → `bind` → call-site kwargs (later wins). |
| `exc_info` | string or null | Formatted traceback when `exc_info=True`; `null` otherwise. |
| `pid` | int | Process id. |
| `thread` | string | Thread name (`record.threadName`). |

Non-JSON-serializable field values are coerced to strings via `default=str`.

## Redaction

`redact=["password", "token"]` replaces matching keys with the literal
`<redacted>` in both text and JSON output. Redaction runs after all
field merges, so a redacted key cannot be reintroduced via `bind` or
`Context`.

## Text output format

Default format string:

```
%(asctime)s %(levelname)s %(name)s: %(message)s
```

Structured fields are appended as `key=value` pairs separated by
spaces. Values containing whitespace or `=` are JSON-quoted.
