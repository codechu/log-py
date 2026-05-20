```text
━━━━━━━━━━━━ c o d e c h u  ·  l o g ━━━━━━━━━━━━

   2026-05-20T12:34:56.789Z  INFO   myapp  started   service=api user=onur
   2026-05-20T12:34:57.013Z  WARN   myapp  retrying  attempt=2 backoff=0.5s
   2026-05-20T12:34:57.812Z  ERROR  myapp  failed    err="ECONNRESET" req=r-42

━━━ one call. structured records. async-safe context. ━━━
```

> *Stdlib-only structured logging — JSON or text, rotating, redacting, `contextvars`-aware.*

[![PyPI](https://img.shields.io/pypi/v/codechu-log.svg)](https://pypi.org/project/codechu-log/)
[![Python](https://img.shields.io/pypi/pyversions/codechu-log.svg)](https://pypi.org/project/codechu-log/)
[![CI](https://github.com/codechu/log-py/actions/workflows/ci.yml/badge.svg)](https://github.com/codechu/log-py/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

# codechu-log

Stdlib-only structured logging for Python. One call sets up a
rotating file handler, a TTY-aware console handler, optional JSON
output, and a redaction list. Context propagates through
`contextvars` so it survives `await` boundaries.

## Install

```bash
pip install codechu-log
```

Python 3.10+. Built on stdlib `logging`; zero third-party deps.

## Quick example

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

## What you get

- **`setup(name, *, level, file, json, max_bytes, backup_count, fmt, redact)`**
  — one-call configuration with `RotatingFileHandler` and a
  TTY-aware console handler.
- **`Context(**fields)`** — `contextvars`-backed scope; nested
  scopes merge, child wins on key conflict, propagation survives
  `await`.
- **`bind(logger, **fields)`** — always-on fields per logger
  instance.
- **`structured(logger)`** —
  `log.info("msg", key=value)` lifts kwargs into the structured
  payload.
- **`redact=[…]`** — listed field keys are replaced with
  `<redacted>` in both text and JSON output.

## Read more

- [API reference](docs/API.md) — every public symbol and the JSON
  schema.
- [Recipes](docs/RECIPES.md) — common configurations.
- [Changelog](CHANGELOG.md)

## Family

| Library | Purpose |
|---------|---------|
| [codechu-events](https://pypi.org/project/codechu-events/) | Thread-safe multi-channel pub/sub bus |
| [codechu-ipc](https://pypi.org/project/codechu-ipc/) | Local IPC — Unix socket, FIFO, JSON-line protocol |
| [codechu-xdg](https://pypi.org/project/codechu-xdg/) | XDG Base Directory helpers, vendor-namespaced |
| [codechu-fmt](https://pypi.org/project/codechu-fmt/) | Human-readable sizes, durations, rates |
| [codechu-fs](https://pypi.org/project/codechu-fs/) | Filesystem primitives — atomic write, XDG trash |

Full ecosystem: [github.com/codechu](https://github.com/codechu).

## Credits

- Built on stdlib `logging`; `contextvars` pattern for async-safe
  context propagation.

## License

MIT — see [LICENSE](LICENSE).

Part of [Codechu](https://github.com/codechu).
