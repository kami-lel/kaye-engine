"""
cli_error_test.py

Unit Tests (using pytest) for:

fmt_unknown, report_unknown
"""

import logging

import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.cli.cli_error import fmt_unknown, report_unknown


class TestFmtUnknown:

    def test_names_noun_and_name(_):
        assert fmt_unknown("glossary", "zzz", ["alpha"]) == (
            "unknown glossary: zzz"
        )

    def test_suggests_the_closest_choice(_):
        assert fmt_unknown("glossary", "alpah", ["alpha", "omega"]) == (
            "unknown glossary: alpah\ndid you mean: alpha"
        )

    def test_no_hint_without_choices(_):
        assert "did you mean" not in fmt_unknown("glossary", "a", [])


class TestReportUnknown:

    def test_logs_an_error_and_exits_1(_, caplog):
        with caplog.at_level(logging.ERROR, logger=LOGGER_NAME):
            with pytest.raises(SystemExit) as info:
                report_unknown("exportable", "nope", ["alpha"])

        assert info.value.code == 1
        assert caplog.records[0].levelno == logging.ERROR
        assert "unknown exportable: nope" in caplog.records[0].message
