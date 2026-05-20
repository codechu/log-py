from __future__ import annotations

import json
from pathlib import Path

from codechu_log import bind, setup, structured


def _lines(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_bind_includes_fields_in_every_call(tmp_path: Path) -> None:
    log_file = tmp_path / "bind.log"
    log = bind(setup("test.bind", file=str(log_file), json=True), service="api")
    log.info("one")
    log.warning("two", request_id="r2")
    for h in log.logger.handlers:
        h.flush()
    one, two = _lines(log_file)
    assert one["fields"] == {"service": "api"}
    assert two["fields"] == {"service": "api", "request_id": "r2"}
    assert two["level"] == "WARNING"


def test_structured_kwargs_become_fields(tmp_path: Path) -> None:
    log_file = tmp_path / "struct.log"
    log = structured(setup("test.struct", file=str(log_file), json=True))
    log.info("hello", user="onur", count=3)
    for h in log.logger.handlers:
        h.flush()
    obj = _lines(log_file)[0]
    assert obj["fields"] == {"user": "onur", "count": 3}


def test_bind_chain_merges(tmp_path: Path) -> None:
    log_file = tmp_path / "chain.log"
    root = setup("test.chain", file=str(log_file), json=True)
    log = bind(root, service="api").bind(version="1")
    log.info("hi", request_id="r")
    for h in root.handlers:
        h.flush()
    obj = _lines(log_file)[0]
    assert obj["fields"] == {"service": "api", "version": "1", "request_id": "r"}


def test_bind_exc_info_passes_through(tmp_path: Path) -> None:
    log_file = tmp_path / "exc.log"
    log = bind(setup("test.exc", file=str(log_file), json=True), service="api")
    try:
        raise ValueError("boom")
    except ValueError:
        log.exception("failed")
    for h in log.logger.handlers:
        h.flush()
    obj = _lines(log_file)[0]
    assert obj["fields"] == {"service": "api"}
    assert obj["exc_info"] is not None
    assert "ValueError: boom" in obj["exc_info"]
