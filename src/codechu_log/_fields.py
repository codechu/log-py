"""Context-var backed structured fields.

A single ``ContextVar`` holds the *merged* dict of fields visible to the
current logical execution (thread, task, or coroutine). ``Context`` is a
context manager that pushes a child scope and restores the parent on exit.
"""

from __future__ import annotations

from contextlib import AbstractContextManager
from contextvars import ContextVar, Token
from typing import Any

_fields: ContextVar[dict[str, Any]] = ContextVar("codechu_log_fields", default={})


def current_fields() -> dict[str, Any]:
    """Snapshot of the structured fields visible to the current scope."""
    return dict(_fields.get())


class Context(AbstractContextManager["Context"]):
    """Attach structured fields to every log emitted inside the ``with`` block.

    Nested contexts merge with parent scope; child keys win on conflict.
    Backed by :mod:`contextvars`, so propagation works across ``await``
    boundaries and ``asyncio.Task`` spawns.
    """

    def __init__(self, **fields: Any) -> None:
        self._fields = fields
        self._token: Token[dict[str, Any]] | None = None

    def __enter__(self) -> Context:
        merged = {**_fields.get(), **self._fields}
        self._token = _fields.set(merged)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._token is not None:
            _fields.reset(self._token)
            self._token = None
