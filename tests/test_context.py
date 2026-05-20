from __future__ import annotations

import asyncio
import json
from pathlib import Path

from codechu_log import Context, setup


def _last_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8").splitlines()[-1])


def test_context_adds_fields(tmp_path: Path) -> None:
    log_file = tmp_path / "ctx.log"
    log = setup("test.ctx.basic", file=str(log_file), json=True)
    with Context(request_id="abc", user="onur"):
        log.info("inside")
    log.info("outside")
    for h in log.handlers:
        h.flush()
    lines = log_file.read_text(encoding="utf-8").splitlines()
    inside = json.loads(lines[0])
    outside = json.loads(lines[1])
    assert inside["fields"] == {"request_id": "abc", "user": "onur"}
    assert outside["fields"] == {}


def test_context_nested_child_wins(tmp_path: Path) -> None:
    log_file = tmp_path / "ctx-nest.log"
    log = setup("test.ctx.nested", file=str(log_file), json=True)
    with Context(user="parent", trace="t1"):
        with Context(user="child"):
            log.info("nested")
    for h in log.handlers:
        h.flush()
    obj = _last_json(log_file)
    assert obj["fields"] == {"user": "child", "trace": "t1"}


def test_context_propagates_across_await(tmp_path: Path) -> None:
    log_file = tmp_path / "ctx-async.log"
    log = setup("test.ctx.async", file=str(log_file), json=True)

    async def inner() -> None:
        await asyncio.sleep(0)
        log.info("from-coroutine")

    async def main() -> None:
        with Context(request_id="async-1"):
            await inner()

    asyncio.run(main())
    for h in log.handlers:
        h.flush()
    obj = _last_json(log_file)
    assert obj["fields"] == {"request_id": "async-1"}
