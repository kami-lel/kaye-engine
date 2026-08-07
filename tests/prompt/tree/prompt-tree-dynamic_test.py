"""
prompt-tree-dynamic_test.py

Unit Tests (using pytest) for:

load_corpus_tree adding dynamic nodes
"""

from unittest.mock import mock_open, patch

import pytest


from kaye_engine.abbr_collection.abbr_data import _abbr_data
from kaye_engine.abbr_collection.abbr_meaning import AbbrMeaning
from kaye_engine.prompt.dynamic_nodes import GlossaryNode
from kaye_engine.prompt.prompt_corpus_loader import load_corpus_tree


# pytest fixtures  #############################################################
@pytest.fixture(scope="session")
def prompt_corpus_tree_preview():
    m = mock_open(read_data="# Title\n")

    with patch("builtins.open", m):
        tree = load_corpus_tree("dynamic-nodes-test", "dummy-path.md")

    return tree.generate_prompt_tree_preview(content_preview_lines=0)


# pytest  ######################################################################
class TestDynamic:
    """
    engine-defined dynamic node types (``DYNAMIC_NODE_TYPES``) still attach
    unconditionally, with no corresponding corpus heading required; abbr
    glossary nodes do not -- they are consumer-defined data, so they only
    attach when a matching ``(glossary-name)`` heading is present, see
    ``TestGlossaryHeading`` below
    """

    def test_today(_, prompt_corpus_tree_preview):
        opt = prompt_corpus_tree_preview

        print(opt)
        assert "── (Today)" in opt

    def test_abbr(_, prompt_corpus_tree_preview):
        opt = prompt_corpus_tree_preview

        print(opt)
        assert "── (Abbreviations)" in opt


class TestGlossaryHeading:

    def test_known_glossary_heading_resolves(_):
        mean = AbbrMeaning("dummy glossary meaning", remark=None)
        with _abbr_data:
            _abbr_data.add_entry(
                mean,
                "dmygrp",
                {
                    "priority": 0,
                    "tags": [],
                    "glossaries": ["some-glossary"],
                    "wrap": "word",
                },
            )

        m = mock_open(
            read_data="# Title\n\n# (some-glossary)\nGlossary preface text.\n"
        )

        with patch("builtins.open", m):
            tree = load_corpus_tree("dynamic-nodes-glossary-test", "d.md")

        node = tree["(some-glossary)"]
        assert isinstance(node, GlossaryNode)
        assert "Glossary preface text." in node.content_lines()

    def test_unknown_glossary_heading_raises(_):
        m = mock_open(read_data="# Title\n\n# (no-such-glossary)\nContent.\n")

        with pytest.raises(
            ValueError, match="unrecognized dynamic node heading"
        ):
            with patch("builtins.open", m):
                load_corpus_tree("dynamic-nodes-glossary-reject-test", "d.md")


class TestPreface:

    def test_matching_heading_becomes_preface(_):
        m = mock_open(
            read_data="# Title\n\n# (Today)\nThe current date, for reference.\n"
        )

        with patch("builtins.open", m):
            tree = load_corpus_tree("dynamic-nodes-preface-test", "d.md")

        today_node = tree["(Today)"]
        assert "The current date, for reference." in today_node.content_lines()

        today_children = [c for c in tree.children if c.name == "(Today)"]
        assert len(today_children) == 1

    def test_unrecognized_paren_heading_raises(_):
        m = mock_open(read_data="# Title\n\n# (Bogus)\nSome content.\n")

        with pytest.raises(ValueError, match="unrecognized dynamic node heading"):
            with patch("builtins.open", m):
                load_corpus_tree("dynamic-nodes-reject-test", "d.md")


class TestNestedParenHeadingRejected:

    def test_unrecognized_nested_paren_heading_raises(_):
        m = mock_open(
            read_data="# Intro\n\n## (Nonsense)\nSome content.\n"
        )

        with pytest.raises(
            ValueError, match="only allowed as a direct child of root"
        ):
            with patch("builtins.open", m):
                load_corpus_tree("dynamic-nodes-nested-reject-test", "d.md")

    def test_recognized_nested_paren_heading_still_raises(_):
        m = mock_open(read_data="# Intro\n\n## (Today)\nSome content.\n")

        with pytest.raises(
            ValueError, match="only allowed as a direct child of root"
        ):
            with patch("builtins.open", m):
                load_corpus_tree("dynamic-nodes-nested-today-test", "d.md")
