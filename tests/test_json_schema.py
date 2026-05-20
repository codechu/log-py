from __future__ import annotations

import json
import os
import re
from pathlib import Path

from codechu_log import setup

ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?\+00:00$")


def test_json_line_schema(tmp_path: Path) -> None:
    log_file = tmp_path / "schema.log"
    log = setup("test.schema", file=str(log_file), json=True)
    log.info("hello")
    for h in log.handlers:
        h.flush()
    obj = json.loads(log_file.read_text(encoding="utf-8").splitlines()[-1])
    assert set(obj.keys()) == {"ts", "level", "logger", "msg", "fields", "exc_info", "pid", "thread"}
    assert ISO_RE.match(obj["ts"]), obj["ts"]
    assert obj["level"] == "INFO"
    assert obj["logger"] == "test.schema"
    assert obj["msg"] == "hello"
    assert obj["fields"] == {}
    assert obj["exc_info"] is None
    assert obj["pid"] == os.getpid()
    assert isinstance(obj["thread"], str) and obj["thread"]
