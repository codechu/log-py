# Recipes

## Console + rotating file, JSON to file only

`setup` uses one formatter for all handlers. To split formats, construct
handlers manually:

```python
import logging
import sys
from logging.handlers import RotatingFileHandler
from codechu_log._format import JsonFormatter, TextFormatter, RedactionFilter

log = logging.getLogger("myapp")
log.setLevel("INFO")

console = logging.StreamHandler(sys.stderr)
console.setFormatter(TextFormatter())
log.addHandler(console)

fh = RotatingFileHandler("app.log", maxBytes=10_000_000, backupCount=5)
fh.setFormatter(JsonFormatter())
fh.addFilter(RedactionFilter(["password", "token"]))
log.addHandler(fh)
```

## Web request scope

```python
from codechu_log import Context, bind, setup

log = bind(setup("api", file="api.log", json=True), service="api")

async def handle(request):
    with Context(request_id=request.headers["x-request-id"]):
        log.info("received", path=request.path)
        return await dispatch(request)
```

`Context` is `contextvars`-backed — concurrent requests do not see each
other's fields.

## Per-task logger via `bind`

```python
worker_log = bind(log, worker_id=worker_id)
worker_log.info("started")
worker_log.info("job", job_id=job_id)
```

## Logging exceptions

```python
try:
    risky()
except Exception:
    log.exception("risky failed", op="risky")
```

`exception` sets `exc_info=True` automatically; the formatted traceback
ends up in the `exc_info` JSON field.
