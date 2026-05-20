from __future__ import annotations

import json
import logging
from pathlib import Path

from codechu_log import bind, setup


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_setup_returns_logger_with_file_handler(tmp_path: Path) -> None:
    log_file = tmp_path / "app.log"
    log = setup("test.setup.text", file=str(log_file))
    log.info("hello world")
    for h in log.handlers:
        h.flush()
    text = _read(log_file)
    assert "hello world" in text
    assert "INFO" in text


def test_setup_json_emits_valid_json_lines(tmp_path: Path) -> None:
    log_file = tmp_path / "app.json.log"
    log = setup("test.setup.json", file=str(log_file), json=True)
    blog = bind(log, service="api")
    blog.info("started", request_id="r1")
    for h in log.handlers:
        h.flush()
    line = _read(log_file).strip().splitlines()[-1]
    obj = json.loads(line)
    assert obj["level"] == "INFO"
    assert obj["logger"] == "test.setup.json"
    assert obj["msg"] == "started"
    assert obj["fields"] == {"service": "api", "request_id": "r1"}
    # schema sanity
    for key in ("ts", "level", "logger", "msg", "fields", "exc_info", "pid", "thread"):
        assert key in obj
    assert obj["exc_info"] is None


def test_setup_idempotent_replaces_handlers(tmp_path: Path) -> None:
    setup("test.setup.idem", file=str(tmp_path / "a.log"))
    log = setup("test.setup.idem", file=str(tmp_path / "b.log"))
    # Exactly one file handler is attached after the second call.
    file_handlers = [h for h in log.handlers if isinstance(h, logging.FileHandler)]
    assert len(file_handlers) == 1
