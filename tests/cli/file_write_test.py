"""
file_write_test.py

Unit Tests (using pytest) for:

write_text_if_changed
"""

import logging
import os

import kamilog
import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.cli.dry_run import disable_dry_run, enable_dry_run
from kaye_engine.cli.file_write import write_text_if_changed

logger = kamilog.getLogger(LOGGER_NAME)


# auxiliaries  #################################################################
@pytest.fixture(autouse=True)
def _reset_dry_run():
    disable_dry_run()
    yield
    disable_dry_run()


def _records(caplog):
    return [(rec.levelno, rec.message) for rec in caplog.records]


def _write(path, content, caplog):
    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        return write_text_if_changed(logger, path, content)


# pytest  ######################################################################
class TestLive:

    def test_missing_file_is_created(_, tmp_path, caplog):
        path = tmp_path / "a.txt"

        assert _write(path, "new", caplog) is True
        assert path.read_text(encoding="utf-8") == "new"
        assert _records(caplog) == [(logging.INFO, "create {}".format(path))]

    def test_same_content_is_skipped(_, tmp_path, caplog):
        path = tmp_path / "a.txt"
        path.write_text("same", encoding="utf-8")
        os.utime(path, (1_000_000, 1_000_000))

        assert _write(path, "same", caplog) is False
        assert path.stat().st_mtime == 1_000_000
        assert _records(caplog) == [
            (kamilog.SKIP, "unchanged {}".format(path))
        ]

    def test_different_content_is_overwritten(_, tmp_path, caplog):
        path = tmp_path / "a.txt"
        path.write_text("old", encoding="utf-8")

        assert _write(path, "new", caplog) is True
        assert path.read_text(encoding="utf-8") == "new"
        assert _records(caplog) == [
            (logging.WARNING, "overwrite {}".format(path))
        ]

    def test_crlf_file_equals_lf_content(_, tmp_path, caplog):
        path = tmp_path / "a.txt"
        path.write_bytes(b"a\r\nb\r\n")

        assert _write(path, "a\nb\n", caplog) is False
        assert path.read_bytes() == b"a\r\nb\r\n"

    def test_undecodable_file_is_overwritten(_, tmp_path, caplog):
        path = tmp_path / "a.txt"
        path.write_bytes(b"\xff\xfe\x00bad")

        assert _write(path, "ok", caplog) is True
        assert path.read_text(encoding="utf-8") == "ok"


class TestDry:

    def test_missing_file_is_reported_not_created(_, tmp_path, caplog):
        enable_dry_run()
        path = tmp_path / "a.txt"

        assert _write(path, "new", caplog) is True
        assert not path.exists()
        assert _records(caplog) == [(logging.INFO, "create {}".format(path))]

    def test_same_content_is_skipped(_, tmp_path, caplog):
        enable_dry_run()
        path = tmp_path / "a.txt"
        path.write_text("same", encoding="utf-8")

        assert _write(path, "same", caplog) is False
        assert _records(caplog) == [
            (kamilog.SKIP, "unchanged {}".format(path))
        ]

    def test_different_content_is_reported_not_written(_, tmp_path, caplog):
        enable_dry_run()
        path = tmp_path / "a.txt"
        path.write_text("old", encoding="utf-8")

        assert _write(path, "new", caplog) is True
        assert path.read_text(encoding="utf-8") == "old"
        assert _records(caplog) == [
            (logging.WARNING, "overwrite {}".format(path))
        ]
