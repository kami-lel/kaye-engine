"""
deed_test.py

Unit Tests (using pytest) for:

track() deed logging
"""

import logging

import kamilog
import pytest

from kaye_engine.badge import MV_BADGE, NEW_BADGE, OWR_BADGE
from kaye_engine.deed import format_size, track

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

    @pytest.mark.parametrize(
        "deed, args, badge",
        [
            ("create_file", ("f",), NEW_BADGE),
            ("create_dir", ("d",), NEW_BADGE),
            ("pack_files", ("a", "b"), NEW_BADGE),
            ("owr_file", ("f",), OWR_BADGE),
            ("mv_file", ("a", "b"), MV_BADGE),
            ("create_zip", ("plugin", "z"), NEW_BADGE),
            ("save_config", ("c",), None),
            ("load_config", ("c",), None),
        ],
    )
    def test_success_carries_deed_badge(_, caplog, deed, args, badge):
        with caplog.at_level(logging.DEBUG, logger=_NAME):
            with getattr(track(_LOGGER), deed)(*args):
                pass

        expected = () if badge is None else (badge,)
        assert caplog.records[0].badges == expected

    def test_failure_carries_no_badge(_, caplog):
        with caplog.at_level(logging.DEBUG, logger=_NAME):
            with pytest.raises(OSError):
                with track(_LOGGER).create_file("f"):
                    raise OSError("denied")

        assert caplog.records[0].badges == ()

    def test_unknown_deed_raises(_):
        with pytest.raises(AttributeError):
            track(_LOGGER).nonexistent


class TestCreateZip:

    def test_stats_fill_the_bracket(_, caplog):
        with caplog.at_level(logging.DEBUG, logger=_NAME):
            with track(_LOGGER).create_zip("plugin", "out/a.zip") as deed:
                deed.stats = "2 skills, 3 KB"

        assert [r.message for r in caplog.records] == [
            "export plugin (2 skills, 3 KB): out/a.zip"
        ]

    def test_no_stats_drops_the_bracket(_, caplog):
        with caplog.at_level(logging.DEBUG, logger=_NAME):
            with track(_LOGGER).create_zip("skill", "a.zip"):
                pass

        assert caplog.records[0].message == "export skill: a.zip"

    def test_failure_logs_cause_and_reraises(_, caplog):
        with caplog.at_level(logging.DEBUG, logger=_NAME):
            with pytest.raises(OSError):
                with track(_LOGGER).create_zip("skill", "a.zip"):
                    raise OSError("full")

        assert caplog.records[0].message == (
            "fail to export skill: a.zip: OSError: full"
        )
        assert caplog.records[0].levelno == logging.ERROR


class TestFormatSize:

    @pytest.mark.parametrize(
        "size, text",
        [
            (0, "0 B"),
            (1023, "1023 B"),
            (3072, "3 KB"),
            (421888, "412 KB"),
            (1153434, "1.1 MB"),
        ],
    )
    def test_formats_largest_fitting_unit(_, size, text):
        assert format_size(size) == text
