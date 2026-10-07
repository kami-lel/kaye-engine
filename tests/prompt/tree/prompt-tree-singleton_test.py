"""
prompt-tree-singleton_test.py

Unit Tests (using pytest) for:

the one-corpus rule of load_corpus_tree, get_corpus_tree and
clear_corpus_tree
"""
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest
from kaye_engine.prompt.prompt_corpus_loader import (
    clear_corpus_tree,
    get_corpus_tree,
    load_corpus_tree,
)


# pytest  ######################################################################
def _load(text="# Title\n"):
    with patch("builtins.open", mock_open(read_data=text)):
        return load_corpus_tree([Path("dummy-path.md")])


class TestSingleton:

    def test_get_returns_loaded_tree(_):
        loaded = _load()

        assert get_corpus_tree() is loaded
        assert get_corpus_tree() is get_corpus_tree()

    def test_get_before_load_raises(_):
        with pytest.raises(ValueError, match="no corpus tree loaded"):
            get_corpus_tree()

    def test_second_load_raises(_):
        _load()

        with pytest.raises(ValueError, match="already loaded"):
            _load("# Other\n")

    def test_clear_allows_reload(_):
        first = _load()

        clear_corpus_tree()
        second = _load("# Other\n")

        assert second is not first
        assert get_corpus_tree() is second

    def test_clear_without_load_is_noop(_):
        clear_corpus_tree()

        with pytest.raises(ValueError):
            get_corpus_tree()
