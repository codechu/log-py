from __future__ import annotations

from pathlib import Path

from codechu_log import setup


def test_rotation_kicks_in_at_max_bytes(tmp_path: Path) -> None:
    log_file = tmp_path / "rot.log"
    log = setup(
        "test.rotation",
        file=str(log_file),
        max_bytes=512,
        backup_count=3,
    )
    payload = "x" * 100
    for i in range(50):
        log.info("%s %s", i, payload)
    for h in log.handlers:
        h.flush()
    # At least one backup file exists once max_bytes is exceeded.
    rotated = list(tmp_path.glob("rot.log.*"))
    assert rotated, "expected at least one rotated backup"
    assert all(p.stat().st_size <= 2048 for p in [log_file, *rotated])
