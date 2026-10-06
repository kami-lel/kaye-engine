"""
deed_test.py

Unit Tests (using pytest) for:

track() deed logging
"""

import logging

import kamilog
import pytest

from kaye_engine.deed import track

_NAME = "kaye.engine.deed-test"
_LOGGER = kamilog.getLogger(_NAME)


# pytest  ######################################################################
class TestTrack:

    def test_success_logs_fixed_wording(_, caplog):
        with caplog.at_level(logging.DEBUG, logger=_NAME):
            with track(_LOGGER).mv_file("a", "b"):
                pass

        assert [r.message for r in caplog.records] == ["move a -> b"]
        assert caplog.records[0].levelno == logging.INFO

    def test_failure_logs_cause_with_traceback_and_reraises(_, caplog):
        with caplog.at_level(logging.DEBUG, logger=_NAME):
            with pytest.raises(OSError):
                with track(_LOGGER).create_file("f"):
                    raise OSError("denied")

        record = caplog.records[0]
        assert record.message == "fail to create f: OSError: denied"
        assert record.levelno == logging.ERROR
        assert record.exc_info is not None

    def test_log_is_attributed_to_the_with_block(_, caplog):
        with caplog.at_level(logging.DEBUG, logger=_NAME):
            with track(_LOGGER).create_dir("d"):
                pass

        assert caplog.records[0].filename == "deed_test.py"

    def test_unknown_deed_raises(_):
        with pytest.raises(AttributeError):
            track(_LOGGER).nonexistent
