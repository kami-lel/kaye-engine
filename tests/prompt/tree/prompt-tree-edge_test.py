"""
prompt-tree-edge_test.py

Unit Tests (using pytest) for:

load_corpus_tree
"""

from pathlib import Path
from unittest.mock import mock_open, patch

from kaye_engine.prompt.prompt_corpus_loader import load_corpus_tree

# pytest #######################################################################


class TestEdge:  # various edge cases

    def test_empty1(_):  # total empty
        m = mock_open(read_data="")

        with patch("builtins.open", m):
            tree = load_corpus_tree("edge-empty1", [Path("dummy-path.md")])
            assert tree.depth == 0
            assert tree.parent is None

    def test_empty2(_):
        m = mock_open(read_data="\n")

        with patch("builtins.open", m):
            tree = load_corpus_tree("edge-empty2", [Path("dummy-path.md")])
            assert tree.depth == 0
            assert tree.parent is None

    def test_empty3(_):
        m = mock_open(read_data="\n" * 10)

        with patch("builtins.open", m):
            tree = load_corpus_tree("edge-empty3", [Path("dummy-path.md")])
            assert tree.depth == 0
            assert tree.parent is None
