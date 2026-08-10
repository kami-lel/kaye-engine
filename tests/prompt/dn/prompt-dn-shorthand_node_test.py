"""
prompt-dn-shorthand_node_test.py

Unit Tests (using pytest) for: ShorthandNode, GlossaryNode,
covering the case where the abbr data singleton is empty
"""

import logging
from unittest.mock import patch

import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.abbr_collection import AbbrData, AbbrMeaning
from kaye_engine.prompt.dynamic_nodes import ShorthandNode, GlossaryNode

_GLOSSARY_NAMES = (
    "usable-abbreviations",
    "coding-terms",
    "programming-language-codes",
    "natural-language-codes",
    "unity-engine-abbr",
    "plan-step-by-step-abbr",
    "code-documentation-field-abbr",
)


# pytest fixture  ##############################################################
@pytest.fixture
def empty_abbr_data():
    return AbbrData()


# GlossaryNode  #################################################################
class TestGlossaryNodesEmpty:

    @pytest.mark.parametrize("glossary_name", _GLOSSARY_NAMES)
    def test_content_lines_empty(_, glossary_name, empty_abbr_data, caplog):
        testee = GlossaryNode(None, glossary_name=glossary_name)

        with patch(
            "kaye_engine.prompt.dynamic_nodes.glossary_node.get_abbr_data",
            return_value=empty_abbr_data,
        ):
            with caplog.at_level(logging.ERROR, logger=LOGGER_NAME):
                opt = testee.content_lines()

        print(opt)
        assert opt == []
        assert any(
            rec.levelno == logging.ERROR for rec in caplog.records
        )

    def test_heading_and_glossary_name(_):
        testee = GlossaryNode(None, glossary_name="coding-terms")

        assert testee.glossary_name == "coding-terms"
        assert testee.name == "(coding-terms)"


# pytest fixture  ##############################################################
@pytest.fixture
def populated_abbr_data():
    data = AbbrData()
    with data:
        data.add_entry(
            AbbrMeaning("for example"),
            "e.g.",
            {"priority": 5, "tags": ["g"], "wrap": "word"},
        )
        data.add_entry(
            AbbrMeaning("id est"),
            "i.e.",
            {"priority": 1, "tags": ["g"], "wrap": "word"},
        )
        data.add_entry(
            AbbrMeaning("et cetera"),
            "etc.",
            {"priority": 3, "tags": ["g"], "wrap": "word"},
        )
    return data


class TestGlossaryNodeSorting:  # =============================================

    def test_content_lines_unsorted(_, populated_abbr_data):
        testee = GlossaryNode(None, glossary_name="g")

        with patch(
            "kaye_engine.prompt.dynamic_nodes.glossary_node.get_abbr_data",
            return_value=populated_abbr_data,
        ):
            opt = testee.content_lines()

        print(opt)
        assert opt == [
            "- e.g.:for example",
            "- i.e.:id est",
            "- etc.:et cetera",
        ]

    def test_content_lines_sorted_bulleted(_, populated_abbr_data):
        testee = GlossaryNode(None, glossary_name="g")

        with patch(
            "kaye_engine.prompt.dynamic_nodes.glossary_node.get_abbr_data",
            return_value=populated_abbr_data,
        ):
            opt = testee.content_lines(is_sorted=True)

        print(opt)
        assert opt == [
            "- i.e.:id est",
            "- etc.:et cetera",
            "- e.g.:for example",
        ]

    def test_content_lines_sorted_numbered(_, populated_abbr_data):
        testee = GlossaryNode(None, glossary_name="g")

        with patch(
            "kaye_engine.prompt.dynamic_nodes.glossary_node.get_abbr_data",
            return_value=populated_abbr_data,
        ):
            opt = testee.content_lines(is_sorted=True, uses_numbered_list=True)

        print(opt)
        assert opt == [
            "1. i.e.:id est",
            "2. etc.:et cetera",
            "3. e.g.:for example",
        ]


# ShorthandNode  ################################################################
class TestShorthandNodeEmpty:

    def test_content_lines_no_query(_, empty_abbr_data, caplog):
        testee = ShorthandNode(None)

        with patch(
            "kaye_engine.prompt.dynamic_nodes.shorthand_tag_nodes.get_abbr_data",
            return_value=empty_abbr_data,
        ):
            with caplog.at_level(logging.ERROR, logger=LOGGER_NAME):
                opt = testee.content_lines()

        print(opt)
        assert opt == []
        assert any(
            rec.levelno == logging.ERROR for rec in caplog.records
        )

    def test_content_lines_with_query(_, empty_abbr_data, caplog):
        testee = ShorthandNode(None)

        with patch(
            "kaye_engine.prompt.dynamic_nodes.shorthand_node.get_abbr_data",
            return_value=empty_abbr_data,
        ):
            with caplog.at_level(logging.ERROR, logger=LOGGER_NAME):
                opt = testee.content_lines(query="use an algo to calc avg")

        print(opt)
        assert opt == []
        assert any(
            rec.levelno == logging.ERROR for rec in caplog.records
        )
