"""
prompt-bp-dynamic_substitution_test.py

Unit Tests (using pytest) for: apply_dynamic_substitutions
"""

import logging

from kaye_engine import LOGGER_NAME
from kaye_engine.abbr_collection.abbr_data import _abbr_data
from kaye_engine.abbr_collection.abbr_meaning import AbbrMeaning
from kaye_engine.prompt.blueprint.dynamic_substitution import (
    apply_dynamic_substitutions,
)


# pytest  ######################################################################
class TestNoPlaceholder:

    def test_returns_text_unchanged(_):
        opt = apply_dynamic_substitutions("no placeholders here")

        assert opt == "no placeholders here"


class TestSinglePlaceholder:

    def test_today_resolves(_):
        opt = apply_dynamic_substitutions("date: (((today)))")

        assert opt.startswith("date: Date: ")
        assert "(((today)))" not in opt


class TestMultiplePlaceholders:

    def test_distinct_names_both_resolve(_):
        opt = apply_dynamic_substitutions(
            "(((today))) -- (((decode-only-shorthand)))"
        )

        assert "(((today)))" not in opt
        assert "(((decode-only-shorthand)))" not in opt
        assert "Date: " in opt


class TestRepeatedPlaceholder:

    def test_same_name_resolves_identically_both_times(_):
        opt = apply_dynamic_substitutions("(((today))) and again (((today)))")

        halves = opt.split(" and again ")
        assert len(halves) == 2
        assert halves[0] == halves[1]


class TestUnresolvedPlaceholder:

    def test_warns_and_leaves_literal_text(_, caplog):
        with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
            opt = apply_dynamic_substitutions("(((bogus)))")

        assert opt == "(((bogus)))"
        assert any(rec.levelno == logging.WARNING for rec in caplog.records)


class TestKwargsThreadThrough:

    def test_query_reaches_shorthand_node(_):
        opt = apply_dynamic_substitutions(
            "(((decode-only-shorthand)))", query=""
        )

        assert "(((decode-only-shorthand)))" not in opt

    def test_glossary_priority_threshold_reaches_glossary_node(_):
        with _abbr_data:
            _abbr_data.add_entry(
                AbbrMeaning("dynamic sub low priority", remark=None),
                "dslop",
                {"priority": 0, "tags": ["some-glossary"], "wrap": "word"},
            )
            _abbr_data.add_entry(
                AbbrMeaning("dynamic sub high priority", remark=None),
                "dship",
                {"priority": 99, "tags": ["some-glossary"], "wrap": "word"},
            )

        low = apply_dynamic_substitutions(
            "(((some-glossary)))", glossary_priority_threshold=0
        )
        high = apply_dynamic_substitutions(
            "(((some-glossary)))", glossary_priority_threshold=99
        )

        assert low != high
