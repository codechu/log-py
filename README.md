# codechu-log

[![PyPI](https://img.shields.io/pypi/v/codechu-log.svg)](https://pypi.org/project/codechu-log/)
[![Python](https://img.shields.io/pypi/pyversions/codechu-log.svg)](https://pypi.org/project/codechu-log/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Stdlib-only structured logging for Python 3.10+. One call configures a
rotating file handler, a TTY-aware console handler, optional JSON output,
and a redaction list. Context is propagated through `contextvars` so it
works across `await` boundaries.

```python
from codechu_log import setup, bind, Context

log = bind(setup("myapp", file="app.log", json=True), service="api")

with Context(request_id="r-42"):
    log.info("started", user="onur")
```

Output (one JSON object per line):

```json
{"ts": "2026-05-20T12:34:56.789012+00:00", "level": "INFO",
 "logger": "myapp", "msg": "started",
 "fields": {"service": "api", "request_id": "r-42", "user": "onur"},
 "exc_info": null, "pid": 4321, "thread": "MainThread"}
```

## Features

- `setup(name, *, level, file, json, max_bytes, backup_count, fmt, redact)`
  — one-call configuration with `RotatingFileHandler` and a TTY-aware
  console handler.
- `Context(**fields)` — context manager backed by `contextvars`; nested
  scopes merge, child wins on key conflict, propagation survives `await`.
- `bind(logger, **fields)` — always-on fields per logger.
- `structured(logger)` — `log.info("msg", key=value)` lifts kwargs into
  the structured payload.
- `redact=[...]` — replace listed field keys with `<redacted>` in both
  text and JSON output.

## Install

```bash
pip install codechu-log
```

## Documentation

- [API reference](docs/API.md) — every public symbol and the JSON schema.
- [Recipes](docs/RECIPES.md) — common configurations.
- [CHANGELOG](CHANGELOG.md)

## License

MIT — see [LICENSE](LICENSE).
