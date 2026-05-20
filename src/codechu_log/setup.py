"""One-call logger setup."""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Iterable

from ._format import JsonFormatter, RedactionFilter, TextFormatter


def _is_tty() -> bool:
    try:
        from codechu_term import is_tty  # type: ignore[import-not-found]

        return bool(is_tty(sys.stderr))
    except Exception:
        return bool(getattr(sys.stderr, "isatty", lambda: False)())


def setup(
    name: str,
    *,
    level: int | str = "INFO",
    file: str | None = None,
    json: bool = False,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    fmt: str | None = None,
    redact: Iterable[str] | None = None,
) -> logging.Logger:
    """Configure and return a :class:`logging.Logger`.

    Parameters
    ----------
    name:
        Logger name (typically a dotted module / app name).
    level:
        Standard ``logging`` level (``"INFO"``, ``logging.DEBUG``, …).
    file:
        Path of a rotating log file. Omit for console-only.
    json:
        When ``True``, every handler emits one JSON object per line.
    max_bytes, backup_count:
        Forwarded to :class:`logging.handlers.RotatingFileHandler`.
    fmt:
        Custom text format string (ignored when ``json=True``).
    redact:
        Iterable of structured-field keys to mask as ``<redacted>``.
        Applies to both text and JSON formatters.
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)
    # Clear any handlers attached by a previous setup() call so the function
    # is idempotent in tests and re-configurations.
    for h in list(logger.handlers):
        logger.removeHandler(h)
    logger.propagate = False

    formatter: logging.Formatter
    if json:
        formatter = JsonFormatter()
    else:
        formatter = TextFormatter(fmt=fmt)

    redact_filter = RedactionFilter(redact or ())

    if _is_tty():
        console = logging.StreamHandler(sys.stderr)
        console.setFormatter(formatter)
        console.addFilter(redact_filter)
        logger.addHandler(console)

    if file:
        fh = RotatingFileHandler(
            file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        fh.setFormatter(formatter)
        fh.addFilter(redact_filter)
        logger.addHandler(fh)

    return logger
