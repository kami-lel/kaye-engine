"""
exportable_abbr_test.py

Unit Tests (using pytest) for:

- get_exportable_abbrs
"""

import logging
from unittest.mock import patch

import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.abbr_collection import AbbrData, AbbrMeaning
from kaye_engine.abbr_collection.abbr_glossary_registry import (
    abbr_glossary_registry,
    register_abbr_glossary,
)
from kaye_engine.cli.exportable_abbr import get_exportable_abbrs


class TestGetExportableAbbrsEmpty:

    def test_returns_empty_list(_, cap_log):
        empty = AbbrData()

        with (
            patch(
                "kaye_engine.cli.exportable_abbr.get_abbr_data",
                return_value=empty,
            ),
            cap_log.at_level(logging.ERROR, logger=LOGGER_NAME),
        ):
            opt = get_exportable_abbrs()

        print(opt)
        assert opt == []
        assert any(rec.levelno == logging.ERROR for rec in cap_log.records)


@pytest.fixture
def registered_names():
    names = []
    yield names
    for name in names:
        abbr_glossary_registry.pop(name, None)


class TestGetExportableAbbrsFiltersByIsExportable:

    def test_excludes_non_exportable_glossary(_, registered_names):
        exportable_reg = register_abbr_glossary(
            "test-glossary-exportable", True
        )
        registered_names.append(exportable_reg.name)
        non_exportable_reg = register_abbr_glossary(
            "test-glossary-non-exportable", False
        )
        registered_names.append(non_exportable_reg.name)

        data = AbbrData()
        with data:
            data.add_entry(
                AbbrMeaning("dummy exportable"),
                "dmy-exp",
                {
                    "priority": 0,
                    "tags": ["test-glossary-exportable"],
                    "wrap": "word",
                },
            )
            data.add_entry(
                AbbrMeaning("dummy non-exportable"),
                "dmy-non-exp",
                {
                    "priority": 0,
                    "tags": ["test-glossary-non-exportable"],
                    "wrap": "word",
                },
            )

        with patch(
            "kaye_engine.cli.exportable_abbr.get_abbr_data",
            return_value=data,
        ):
            opt = get_exportable_abbrs()

        canonical_names = [group.canonical_name for group in opt]
        assert "abbr-glossary-test-glossary-exportable" in canonical_names
        assert (
            "abbr-glossary-test-glossary-non-exportable" not in canonical_names
        )
