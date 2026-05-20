```text
   c o d e c h u  ·  l o g
   2026-05-20T12:34:56.789Z  INFO  myapp  started  service=api user=onur
   2026-05-20T12:34:57.013Z  WARN  myapp  retrying  attempt=2 backoff=0.5s
   2026-05-20T12:34:57.812Z  ERROR myapp  failed    err="ECONNRESET" req=r-42
   ── one call. structured records. async-safe context. ──
```

> *Stdlib-only structured logging — JSON or text, rotating, redacting, `contextvars`-aware.*

[![PyPI](https://img.shields.io/pypi/v/codechu-log.svg)](https://pypi.org/project/codechu-log/)
[![Python](https://img.shields.io/pypi/pyversions/codechu-log.svg)](https://pypi.org/project/codechu-log/)
[![CI](https://github.com/codechu/log-py/actions/workflows/ci.yml/badge.svg)](https://github.com/codechu/log-py/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

# codechu-log

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

## Codechu family

Companion libraries from the Codechu Python ecosystem:

| Library | Purpose |
|---------|---------|
| [codechu-fmt](https://pypi.org/project/codechu-fmt/) | Human-readable formatting — sizes, durations, rates, percent |
| [codechu-meter](https://pypi.org/project/codechu-meter/) | Timing primitives — Stopwatch, ETA, percentile, histogram |
| [codechu-spark](https://pypi.org/project/codechu-spark/) | Unicode sparklines, mini bar charts, heatmaps |
| [codechu-cli](https://pypi.org/project/codechu-cli/) | CLI primitives — colors, progress, spinners, prompts, table |
| [codechu-events](https://pypi.org/project/codechu-events/) | Thread-safe multi-channel pub/sub bus with replay |
| [codechu-xdg](https://pypi.org/project/codechu-xdg/) | XDG Base Directory helpers, vendor-namespaced |
| [codechu-treeviz](https://pypi.org/project/codechu-treeviz/) | Tree visualization — treemap, sunburst, icicle, flame |
| [codechu-fs](https://pypi.org/project/codechu-fs/) | Filesystem primitives — atomic write, XDG trash, safe walk |
| [codechu-term](https://pypi.org/project/codechu-term/) | Terminal capability detection, alt buffer, raw mode |
| [codechu-color](https://pypi.org/project/codechu-color/) | Color palettes, WCAG contrast, color-blind variants |
| [codechu-treedata](https://pypi.org/project/codechu-treedata/) | N-ary tree data structures and algorithms |
| [codechu-i18n](https://pypi.org/project/codechu-i18n/) | Internationalization — locale, plural rules, RTL |
| [codechu-ipc](https://pypi.org/project/codechu-ipc/) | Local IPC — Unix socket, FIFO, JSON-line protocol |
| [codechu-config](https://pypi.org/project/codechu-config/) | Schema-driven config — atomic save, migrations |

## Credits

- Built on stdlib `logging`; contextvars pattern for async-safe context propagation.

## License

MIT — see [LICENSE](LICENSE).
