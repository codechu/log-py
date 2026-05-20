"""Formatters and the redaction filter.

Two formatters share one rule: structured fields live on the ``LogRecord``
attribute ``_fields`` (a dict). They are *merged* lazily from
:data:`codechu_log._fields._fields` at emit time so that ``Context`` works
even for already-bound loggers.
"""

from __future__ import annotations

import json
import logging
import os
import threading
from datetime import datetime, timezone
from typing import Any, Iterable

from ._fields import current_fields

REDACTED = "<redacted>"


def _gather_fields(record: logging.LogRecord) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    fields.update(current_fields())
    extra = getattr(record, "_fields", None)
    if extra:
        fields.update(extra)
    return fields


def _redact(fields: dict[str, Any], keys: frozenset[str]) -> dict[str, Any]:
    if not keys:
        return fields
    return {k: (REDACTED if k in keys else v) for k, v in fields.items()}


class RedactionFilter(logging.Filter):
    """Marks the redaction set on each record; formatters apply it."""

    def __init__(self, keys: Iterable[str]) -> None:
        super().__init__()
        self.keys = frozenset(keys)

    def filter(self, record: logging.LogRecord) -> bool:
        record._redact_keys = self.keys  # type: ignore[attr-defined]
        return True


def _record_redact_keys(record: logging.LogRecord) -> frozenset[str]:
    return getattr(record, "_redact_keys", frozenset())


class JsonFormatter(logging.Formatter):
    """Emit one JSON object per record.

    Schema (see ``docs/API.md``):
    ``ts`` ISO-8601 UTC, ``level``, ``logger``, ``msg``, ``fields`` dict,
    ``exc_info`` str|null, ``pid`` int, ``thread`` str.
    """

    def format(self, record: logging.LogRecord) -> str:
        fields = _redact(_gather_fields(record), _record_redact_keys(record))
        payload: dict[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "fields": fields,
            "exc_info": self.formatException(record.exc_info) if record.exc_info else None,
            "pid": os.getpid(),
            "thread": record.threadName or threading.current_thread().name,
        }
        return json.dumps(payload, default=str, ensure_ascii=False)


class TextFormatter(logging.Formatter):
    """Human-friendly format: ``ts LEVEL logger: msg key=value …``."""

    default_time_format = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, fmt: str | None = None) -> None:
        super().__init__(fmt=fmt or "%(asctime)s %(levelname)s %(name)s: %(message)s")

    def format(self, record: logging.LogRecord) -> str:
        base = super().format(record)
        fields = _redact(_gather_fields(record), _record_redact_keys(record))
        if not fields:
            return base
        suffix = " ".join(f"{k}={_render_value(v)}" for k, v in fields.items())
        return f"{base} {suffix}"


def _render_value(v: Any) -> str:
    s = str(v)
    if any(ch.isspace() for ch in s) or "=" in s:
        return json.dumps(s, ensure_ascii=False)
    return s
