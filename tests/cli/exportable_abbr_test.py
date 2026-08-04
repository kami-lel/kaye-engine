"""
exportable_abbr_test.py

Unit Tests (using pytest) for:

- get_exportable_abbrs
"""

import logging
from unittest.mock import patch

from kaye_engine import LOGGER_NAME
from kaye_engine.abbr_collection import AbbrData
from kaye_engine.cli.exportable_abbr import get_exportable_abbrs


class TestGetExportableAbbrsEmpty:

    def test_returns_empty_list(_, caplog):
        empty = AbbrData()

        with patch(
            "kaye_engine.cli.exportable_abbr.get_abbr_data",
            return_value=empty,
        ):
            with caplog.at_level(logging.ERROR, logger=LOGGER_NAME):
                opt = get_exportable_abbrs()

        print(opt)
        assert opt == []
        assert any(rec.levelno == logging.ERROR for rec in caplog.records)
