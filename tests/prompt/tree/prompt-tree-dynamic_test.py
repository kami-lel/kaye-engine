"""
prompt-tree-dynamic_test.py

Unit Tests (using pytest) for:

load_corpus_tree adding dynamic nodes
"""

from unittest.mock import mock_open, patch

import pytest


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

    def test_today(_, prompt_corpus_tree_preview):
        opt = prompt_corpus_tree_preview

        print(opt)
        assert "── (Today)" in opt

    def test_abbr(_, prompt_corpus_tree_preview):
        opt = prompt_corpus_tree_preview

        print(opt)
        assert "── (Abbreviations)" in opt

    def test_usable(_, prompt_corpus_tree_preview):
        opt = prompt_corpus_tree_preview

        print(opt)
        assert "── (Usable Abbreviations)" in opt

    def test_lc(_, prompt_corpus_tree_preview):
        opt = prompt_corpus_tree_preview

        print(opt)
        assert "── (Languages Code)" in opt

    def test_plc(_, prompt_corpus_tree_preview):
        opt = prompt_corpus_tree_preview

        print(opt)
        assert "── (Programming Languages Code)" in opt

    def test_u3d(_, prompt_corpus_tree_preview):
        opt = prompt_corpus_tree_preview

        print(opt)
        assert "── (Unity Engine Abbreviations)" in opt
