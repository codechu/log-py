"""codechu-log — stdlib-only structured logging.

Public API:

- :func:`setup`      — one-call configuration (file rotation, console, JSON, redaction).
- :class:`Context`   — contextvars-backed structured field scope.
- :func:`bind`       — wrap a logger with always-on fields.
- :func:`structured` — wrap a logger so ``**kwargs`` become structured fields.
"""

from __future__ import annotations

from ._fields import Context
from .bind import StructuredLogger, bind, structured
from .setup import setup

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "Context",
    "StructuredLogger",
    "bind",
    "setup",
    "structured",
]
