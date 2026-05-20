from __future__ import annotations

import json
from pathlib import Path

from codechu_log import bind, setup


def test_redaction_json(tmp_path: Path) -> None:
    log_file = tmp_path / "redact.log"
    log = bind(
        setup("test.redact.json", file=str(log_file), json=True, redact=["password", "token"]),
        service="api",
    )
    log.info("login", user="onur", password="hunter2", token="abc")
    for h in log.logger.handlers:
        h.flush()
    obj = json.loads(log_file.read_text(encoding="utf-8").splitlines()[0])
    assert obj["fields"]["password"] == "<redacted>"
    assert obj["fields"]["token"] == "<redacted>"
    assert obj["fields"]["user"] == "onur"
    assert obj["fields"]["service"] == "api"


def test_redaction_text(tmp_path: Path) -> None:
    log_file = tmp_path / "redact.txt"
    log = bind(
        setup("test.redact.text", file=str(log_file), redact=["secret"]),
        service="api",
    )
    log.info("ok", secret="s3cr3t", visible="yes")
    for h in log.logger.handlers:
        h.flush()
    text = log_file.read_text(encoding="utf-8")
    assert "s3cr3t" not in text
    assert "secret=<redacted>" in text
    assert "visible=yes" in text
