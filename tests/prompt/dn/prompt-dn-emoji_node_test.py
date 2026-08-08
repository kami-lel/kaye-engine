"""
prompt-dn-emoji_node_test.py

Unit Tests (using pytest) for: EmojiNode
"""

import logging
from unittest.mock import patch

import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.abbr_collection import AbbrData, AbbrMeaning
from kaye_engine.prompt.dynamic_nodes import EmojiNode


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
            {"priority": 18, "tags": ["emoji"], "wrap": "symbol", "glossaries": []},
        )
        data.add_entry(
            AbbrMeaning("agent,AI"),
            "🤖",
            {"priority": 10, "tags": ["emoji"], "wrap": "symbol", "glossaries": []},
        )
        data.add_entry(
            AbbrMeaning("for example"),
            "e.g.",
            {"priority": 5, "tags": [], "wrap": "word", "glossaries": ["g"]},
        )
    return data


# EmojiNode  #####################################################################
class TestEmojiNodeEmpty:

    def test_content_lines_empty(_, empty_abbr_data, caplog):
        testee = EmojiNode(None)

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
        testee = EmojiNode(None)

        assert testee.name == "(Emoji)"


class TestEmojiNodeFiltering:

    def test_content_lines_only_emoji_tagged(_, populated_abbr_data):
        testee = EmojiNode(None)

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
