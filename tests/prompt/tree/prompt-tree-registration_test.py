"""
prompt-tree-registration_test.py

Unit Tests (using pytest) for: register_corpus_under_node, building the
tree with load_corpus_tree from registrations alone
"""

import pytest

from kaye_engine.prompt.prompt_corpus_loader import (
    clear_corpus_tree,
    load_corpus_tree,
    register_corpus_under_node,
)


# pytest fixtures  #############################################################
@pytest.fixture(autouse=True)
def _clean_corpus():
    clear_corpus_tree()
    yield
    clear_corpus_tree()


def _static_names(node):
    return [c.name for c in node.children if not c.name.startswith("(")]


# pytest  ######################################################################
class TestStructure:

    def test_root_registrations_build_tree(_):
        register_corpus_under_node((), "# A\nContent A.\n")
        register_corpus_under_node((), "# B\nContent B.\n")

        tree = load_corpus_tree()

        assert _static_names(tree) == ["A", "B"]
        assert tree["A"].content_lines() == ["Content A.", ""]

    def test_source_under_node(_):
        register_corpus_under_node((), "# A\nContent A.\n## a1\n")
        register_corpus_under_node(("A",), "## a2\nContent a2.\n")

        tree = load_corpus_tree()

        assert _static_names(tree["A"]) == ["a1", "a2"]
        assert tree["A"]["a2"].depth == 2

    def test_str_node_path_is_one_heading(_):
        register_corpus_under_node((), "# A\n")
        register_corpus_under_node("A", "## a1\n")

        tree = load_corpus_tree()

        assert _static_names(tree["A"]) == ["a1"]

    def test_clear_drops_registrations(_):
        register_corpus_under_node((), "# A\n")
        load_corpus_tree()
        clear_corpus_tree()

        tree = load_corpus_tree()

        assert _static_names(tree) == []
