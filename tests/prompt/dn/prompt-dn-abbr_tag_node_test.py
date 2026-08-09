"""
prompt-dn-abbr_tag_node_test.py

Unit Tests (using pytest) for: AbbrTagNode
"""

import logging
from unittest.mock import patch

import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.abbr_collection import AbbrData, AbbrMeaning, AbbrTags
from kaye_engine.prompt.dynamic_nodes import AbbrTagNode


# pytest fixture  ##############################################################
@pytest.fixture
def empty_abbr_data():
    return AbbrData()


@pytest.fixture
def populated_abbr_data():
    data = AbbrData()
    with data:
        data.add_entry(
            AbbrMeaning("package,packaging"),
            "📦",
            {"priority": 18, "tags": ["emoji"], "wrap": "symbol"},
        )
        data.add_entry(
            AbbrMeaning("agent,AI"),
            "🤖",
            {"priority": 10, "tags": ["emoji"], "wrap": "symbol"},
        )
        data.add_entry(
            AbbrMeaning("for example"),
            "e.g.",
            {"priority": 5, "tags": ["g"], "wrap": "word"},
        )
    return data


# AbbrTagNode  ####################################################################
class TestAbbrTagNodeEmpty:

    def test_content_lines_empty(_, empty_abbr_data, caplog):
        testee = AbbrTagNode(None, abbr_tag=AbbrTags.emoji)

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

    def test_heading(_):
        testee = AbbrTagNode(None, abbr_tag=AbbrTags.emoji)

        assert testee.name == "(Emoji)"


class TestAbbrTagNodeFiltering:

    def test_content_lines_only_emoji_tagged(_, populated_abbr_data):
        testee = AbbrTagNode(None, abbr_tag=AbbrTags.emoji)

        with patch(
            "kaye_engine.prompt.dynamic_nodes.shorthand_tag_nodes.get_abbr_data",
            return_value=populated_abbr_data,
        ):
            opt = testee.content_lines()

        print(opt)
        assert opt == [
            "- 📦:package,packaging",
            "- 🤖:agent,AI",
        ]


class TestAbbrTagNodeGenericity:
    """
    prove ``AbbrTagNode`` is parametrized over any ``AbbrTags`` member,
    not hardcoded to ``emoji`` -- mirrors ``GlossaryNode`` construction
    """

    def test_heading_for_a_different_abbr_tag(_):
        testee = AbbrTagNode(None, abbr_tag=AbbrTags.single_character)

        assert testee.name == "(Single Character)"

    def test_copy_preserves_abbr_tag(_):
        testee = AbbrTagNode(None, abbr_tag=AbbrTags.single_character)

        opt = testee.__copy__()

        assert opt.abbr_tag == AbbrTags.single_character
        assert opt.name == "(Single Character)"
