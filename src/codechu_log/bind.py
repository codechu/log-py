"""Logger wrappers — :func:`bind` and :func:`structured`.

Both produce a :class:`StructuredLogger` whose ``info``/``warning``/… calls
accept arbitrary ``**fields`` keyword arguments. ``bind`` additionally
seeds a set of always-on fields.
"""

from __future__ import annotations

import logging
from typing import Any

_RESERVED = {"exc_info", "stack_info", "stacklevel", "extra"}


class StructuredLogger:
    """A thin façade over :class:`logging.Logger` that lifts ``**fields``
    into the structured payload of every emitted record.

    Methods mirror the standard logger (``debug`` … ``critical`` plus
    ``log`` and ``exception``); reserved ``logging`` kwargs are passed
    through untouched.
    """

    def __init__(self, logger: logging.Logger, fields: dict[str, Any] | None = None) -> None:
        self._logger = logger
        self._bound: dict[str, Any] = dict(fields or {})

    # logger-like methods ------------------------------------------------

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.DEBUG, msg, args, kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.INFO, msg, args, kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.WARNING, msg, args, kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.ERROR, msg, args, kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.CRITICAL, msg, args, kwargs)

    def exception(self, msg: str, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("exc_info", True)
        self._log(logging.ERROR, msg, args, kwargs)

    def log(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(level, msg, args, kwargs)

    # composition --------------------------------------------------------

    def bind(self, **fields: Any) -> StructuredLogger:
        """Return a new wrapper with additional bound fields."""
        merged = {**self._bound, **fields}
        return StructuredLogger(self._logger, merged)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    # internals ----------------------------------------------------------

    def _log(self, level: int, msg: str, args: tuple, kwargs: dict[str, Any]) -> None:
        passthrough = {k: kwargs.pop(k) for k in list(kwargs) if k in _RESERVED}
        fields = {**self._bound, **kwargs}
        extra = passthrough.pop("extra", None) or {}
        extra = {**extra, "_fields": fields}
        self._logger.log(level, msg, *args, extra=extra, **passthrough)


def bind(logger: logging.Logger | StructuredLogger, **fields: Any) -> StructuredLogger:
    """Return a :class:`StructuredLogger` that injects ``fields`` into every call."""
    if isinstance(logger, StructuredLogger):
        return logger.bind(**fields)
    return StructuredLogger(logger, fields)


def structured(logger: logging.Logger | StructuredLogger) -> StructuredLogger:
    """Wrap ``logger`` so that ``log.info("msg", key=value)`` adds fields.

    Equivalent to :func:`bind` with no initial fields.
    """
    return bind(logger)
