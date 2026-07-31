"""
prompt-tree-singleton_test.py

Unit Tests (using pytest) for:

get_corpus_tree caching the tree it was registered under via
load_corpus_tree
"""

from unittest.mock import mock_open, patch

from kaye_engine.prompt.prompt_corpus_loader import (
    load_corpus_tree,
    get_corpus_tree,
)


# pytest  ######################################################################
class TestSingleton:

    def test1(_):
        m = mock_open(read_data="# Title\n")

        with patch("builtins.open", m):
            loaded = load_corpus_tree("singleton-test", "dummy-path.md")

        attempt1 = get_corpus_tree("singleton-test")
        attempt2 = get_corpus_tree("singleton-test")
        attempt3 = get_corpus_tree("singleton-test")

        assert loaded is attempt1
        assert attempt1 is attempt2
        assert attempt2 is attempt3
