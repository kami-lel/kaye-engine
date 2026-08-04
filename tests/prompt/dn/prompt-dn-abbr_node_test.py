"""
prompt-dn-abbr_node_test.py

Unit Tests (using pytest) for: AbbrNode, _AbbrTagNodeBase subclasses,
covering the case where the abbr data singleton is empty
"""

import logging
from unittest.mock import patch

import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.abbr_collection import AbbrData
from kaye_engine.prompt.dynamic_nodes import (
    AbbrNode,
    UsableAbbrNode,
    CodingTermsNode,
    PLCNode,
    LanguageCodeNode,
    UnityEngineAbbrNode,
    PlanStepByStepAbbrNode,
)

_TAG_NODE_TYPES = (
    UsableAbbrNode,
    CodingTermsNode,
    PLCNode,
    LanguageCodeNode,
    UnityEngineAbbrNode,
    PlanStepByStepAbbrNode,
)


# pytest fixture  ##############################################################
@pytest.fixture
def empty_abbr_data():
    return AbbrData()


# abbr-tag nodes  ###############################################################
class TestAbbrTagNodesEmpty:

    @pytest.mark.parametrize("node_cls", _TAG_NODE_TYPES)
    def test_content_lines_empty(_, node_cls, empty_abbr_data, caplog):
        testee = node_cls(None)

        with patch(
            "kaye_engine.prompt.dynamic_nodes.abbr_tag_nodes.get_abbr_data",
            return_value=empty_abbr_data,
        ):
            with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
                opt = testee.content_lines()

        print(opt)
        assert opt == []
        assert any(
            rec.levelno == logging.WARNING for rec in caplog.records
        )


# AbbrNode  #####################################################################
class TestAbbrNodeEmpty:

    def test_content_lines_no_query(_, empty_abbr_data, caplog):
        testee = AbbrNode(None)

        with patch(
            "kaye_engine.prompt.dynamic_nodes.abbr_tag_nodes.get_abbr_data",
            return_value=empty_abbr_data,
        ):
            with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
                opt = testee.content_lines()

        print(opt)
        assert opt == []
        assert any(
            rec.levelno == logging.WARNING for rec in caplog.records
        )

    def test_content_lines_with_query(_, empty_abbr_data, caplog):
        testee = AbbrNode(None)

        with patch(
            "kaye_engine.prompt.dynamic_nodes.abbr_nodes.get_abbr_data",
            return_value=empty_abbr_data,
        ):
            with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
                opt = testee.content_lines(query="use an algo to calc avg")

        print(opt)
        assert opt == []
        assert any(
            rec.levelno == logging.WARNING for rec in caplog.records
        )
