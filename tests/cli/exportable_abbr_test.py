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

    def test_returns_empty_list(_, caplog):
        empty = AbbrData()

        with (
            patch(
                "kaye_engine.cli.exportable_abbr.get_abbr_data",
                return_value=empty,
            ),
            caplog.at_level(logging.ERROR, logger=LOGGER_NAME),
        ):
            opt = get_exportable_abbrs()

        print(opt)
        assert opt == []
        assert any(rec.levelno == logging.ERROR for rec in caplog.records)


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


class TestGetExportableAbbrsGlossaryUserInvokable:

    def test_defaults_to_user_invokable(_, registered_names):
        reg = register_abbr_glossary("test-glossary-default-invokable", True)
        registered_names.append(reg.name)

        data = AbbrData()
        with data:
            data.add_entry(
                AbbrMeaning("dummy"),
                "dmy",
                {
                    "priority": 0,
                    "tags": ["test-glossary-default-invokable"],
                    "wrap": "word",
                },
            )

        with patch(
            "kaye_engine.cli.exportable_abbr.get_abbr_data",
            return_value=data,
        ):
            opt = get_exportable_abbrs()

        group = next(
            g
            for g in opt
            if g.canonical_name
            == "abbr-glossary-test-glossary-default-invokable"
        )
        assert group.is_user_invokable is True
        assert group.llm_invokable is True

    def test_honors_user_invokable_false(_, registered_names):
        reg = register_abbr_glossary(
            "test-glossary-llm-only", True, is_user_invokable=False
        )
        registered_names.append(reg.name)

        data = AbbrData()
        with data:
            data.add_entry(
                AbbrMeaning("dummy"),
                "dmy",
                {
                    "priority": 0,
                    "tags": ["test-glossary-llm-only"],
                    "wrap": "word",
                },
            )

        with patch(
            "kaye_engine.cli.exportable_abbr.get_abbr_data",
            return_value=data,
        ):
            opt = get_exportable_abbrs()

        group = next(
            g
            for g in opt
            if g.canonical_name == "abbr-glossary-test-glossary-llm-only"
        )
        assert group.is_user_invokable is False
        assert group.llm_invokable is True

    def test_tag_wrap_starts_with_groups_are_always_llm_only(
        _, registered_names
    ):
        data = AbbrData()
        with data:
            data.add_entry(
                AbbrMeaning("dummy"),
                "dmy",
                {"priority": 0, "tags": [], "wrap": "word"},
            )

        with patch(
            "kaye_engine.cli.exportable_abbr.get_abbr_data",
            return_value=data,
        ):
            opt = get_exportable_abbrs()

        non_glossary_groups = [
            g
            for g in opt
            if not g.canonical_name.startswith("abbr-glossary-")
        ]
        assert non_glossary_groups
        assert all(g.is_user_invokable is False for g in non_glossary_groups)
        assert all(g.llm_invokable is True for g in non_glossary_groups)
