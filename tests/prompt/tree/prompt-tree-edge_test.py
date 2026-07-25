"""
prompt-tree-edge_test.py

Unit Tests (using pytest) for:

load_prompt_corpus_tree
"""

from unittest.mock import mock_open, patch

from kaye_engine.prompt.prompt_corpus_loader import load_prompt_corpus_tree

# pytest #######################################################################


class TestEdge:  # various edge cases

    def test_empty1(_):  # total empty
        m = mock_open(read_data="")

        with patch("builtins.open", m), patch(
            "kaye_engine.prompt.prompt_corpus_loader.prompt_corpus_tree", new=None
        ):
            tree = load_prompt_corpus_tree()
            assert tree.depth == 0
            assert tree.parent is None

    def test_empty2(_):
        m = mock_open(read_data="\n")

        with patch("builtins.open", m), patch(
            "kaye_engine.prompt.prompt_corpus_loader.prompt_corpus_tree", new=None
        ):
            tree = load_prompt_corpus_tree()
            assert tree.depth == 0
            assert tree.parent is None

    def test_empty3(_):
        m = mock_open(read_data="\n" * 10)

        with patch("builtins.open", m), patch(
            "kaye_engine.prompt.prompt_corpus_loader.prompt_corpus_tree", new=None
        ):
            tree = load_prompt_corpus_tree()
            assert tree.depth == 0
            assert tree.parent is None


class TestAllowsDynamicNodeHeadingSyntax:  #####################################

    def test1(_):
        m = mock_open(read_data="""# Title
## (Some)""")
        with patch("builtins.open", m), patch(
            "kaye_engine.prompt.prompt_corpus_loader.prompt_corpus_tree", new=None
        ):
            tree = load_prompt_corpus_tree()

            node = tree["Title"]["(Some)"]
            print(node)
            assert node.name == "(Some)"
