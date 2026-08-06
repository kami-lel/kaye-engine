"""
prompt-dn-abbr_node_test.py

Unit Tests (using pytest) for: AbbrNode, AbbrGroupNode,
covering the case where the abbr data singleton is empty
"""

import logging
from unittest.mock import patch

import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.abbr_collection import AbbrData, AbbrMeaning
from kaye_engine.prompt.dynamic_nodes import AbbrNode, AbbrGroupNode

_GROUP_NAMES = (
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


# AbbrGroupNode  #################################################################
class TestAbbrGroupNodesEmpty:

    @pytest.mark.parametrize("group_name", _GROUP_NAMES)
    def test_content_lines_empty(_, group_name, empty_abbr_data, caplog):
        testee = AbbrGroupNode(None, group_name=group_name)

        with patch(
            "kaye_engine.prompt.dynamic_nodes.abbr_group_node.get_abbr_data",
            return_value=empty_abbr_data,
        ):
            with caplog.at_level(logging.ERROR, logger=LOGGER_NAME):
                opt = testee.content_lines()

        print(opt)
        assert opt == []
        assert any(
            rec.levelno == logging.ERROR for rec in caplog.records
        )

    def test_heading_and_group_name(_):
        testee = AbbrGroupNode(None, group_name="coding-terms")

        assert testee.group_name == "coding-terms"
        assert testee.name == "(coding-terms)"


# pytest fixture  ##############################################################
@pytest.fixture
def populated_abbr_data():
    data = AbbrData()
    with data:
        data.add_entry(
            AbbrMeaning("for example"),
            "e.g.",
            {"priority": 5, "tags": [], "wrap": "word", "groups": ["g"]},
        )
        data.add_entry(
            AbbrMeaning("id est"),
            "i.e.",
            {"priority": 1, "tags": [], "wrap": "word", "groups": ["g"]},
        )
        data.add_entry(
            AbbrMeaning("et cetera"),
            "etc.",
            {"priority": 3, "tags": [], "wrap": "word", "groups": ["g"]},
        )
    return data


class TestAbbrGroupNodeSorting:  # =============================================

    def test_content_lines_unsorted(_, populated_abbr_data):
        testee = AbbrGroupNode(None, group_name="g")

        with patch(
            "kaye_engine.prompt.dynamic_nodes.abbr_group_node.get_abbr_data",
            return_value=populated_abbr_data,
        ):
            opt = testee.content_lines()

        print(opt)
        assert opt == [
            "- e.g.:for example",
            "- i.e.:id est",
            "- etc.:et cetera",
        ]

    def test_content_lines_sorted(_, populated_abbr_data):
        testee = AbbrGroupNode(None, group_name="g")

        with patch(
            "kaye_engine.prompt.dynamic_nodes.abbr_group_node.get_abbr_data",
            return_value=populated_abbr_data,
        ):
            opt = testee.content_lines(is_sorted=True)

        print(opt)
        assert opt == [
            "1. i.e.:id est",
            "2. etc.:et cetera",
            "3. e.g.:for example",
        ]


# AbbrNode  #####################################################################
class TestAbbrNodeEmpty:

    def test_content_lines_no_query(_, empty_abbr_data, caplog):
        testee = AbbrNode(None)

        with patch(
            "kaye_engine.prompt.dynamic_nodes.abbr_tag_nodes.get_abbr_data",
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
        testee = AbbrNode(None)

        with patch(
            "kaye_engine.prompt.dynamic_nodes.abbr_nodes.get_abbr_data",
            return_value=empty_abbr_data,
        ):
            with caplog.at_level(logging.ERROR, logger=LOGGER_NAME):
                opt = testee.content_lines(query="use an algo to calc avg")

        print(opt)
        assert opt == []
        assert any(
            rec.levelno == logging.ERROR for rec in caplog.records
        )
