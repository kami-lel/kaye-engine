"""
prompt-index-core_test.py

Unit Tests (using pytest) for:

get_corpus_index, CorpusIndex structural arrays
"""

import pytest
from anytree import PreOrderIter

from kaye_engine.prompt.blueprint.index import get_corpus_index
from kaye_engine.prompt.prompt_corpus_loader import (
    clear_corpus_tree,
    get_corpus_tree,
    load_corpus_tree,
)

_STATIC = "# A\nA body.\n## B\n## C\n### D\n# E\n"


# pytest fixtures  #############################################################
@pytest.fixture(params=["static", "singleton", "empty"])
def tree(request):
    sources = {
        "static": [_STATIC],
        "singleton": ["# Only\n"],
        "empty": [],
    }[request.param]
    return load_corpus_tree(sources)


# pytest  ######################################################################
class TestAgreesWithWalk:

    def test_order(_, tree):
        index = get_corpus_index()

        assert list(index.node_objs) == list(PreOrderIter(tree))
        assert all(a is b for a, b in zip(index.node_objs, PreOrderIter(tree)))

    def test_paths_and_depths(_, tree):
        index = get_corpus_index()

        for idx, node in enumerate(index.node_objs):
            assert index.paths[idx] == tuple(n.name for n in node.path[1:])
            assert index.depths[idx] == node.depth
            assert index.idx_by_path[index.paths[idx]] == idx

        assert index.paths[0] == ()

    def test_parents_and_children(_, tree):
        index = get_corpus_index()

        assert index.parent_idxs[0] == -1
        for idx, node in enumerate(index.node_objs):
            if not node.is_root:
                assert index.node_objs[index.parent_idxs[idx]] is node.parent
            assert [index.node_objs[i] for i in index.child_idxs[idx]] == list(
                node.children
            )

    def test_subtree_masks(_, tree):
        index = get_corpus_index()

        for idx, node in enumerate(index.node_objs):
            expected = 0
            for member in PreOrderIter(node):
                expected |= 1 << index.node_objs.index(member)
            assert index.subtree_masks[idx] == expected

        assert index.subtree_masks[0] == (1 << len(index.node_objs)) - 1


class TestStaticShape:

    def test_named_paths(_):
        load_corpus_tree([_STATIC])
        index = get_corpus_index()

        assert ("A",) in index.idx_by_path
        assert ("A", "C", "D") in index.idx_by_path
        assert index.idx_by_path[("A",)] < index.idx_by_path[("A", "B")]
        assert index.idx_by_path[("A", "C", "D")] < index.idx_by_path[("E",)]


class TestLifetime:

    def test_built_once(_, tree):
        assert get_corpus_index() is get_corpus_index()

    def test_get_before_load_raises(_):
        with pytest.raises(ValueError):
            get_corpus_index()

    def test_clear_drops_index(_):
        load_corpus_tree(["# One\n"])
        first = get_corpus_index()

        clear_corpus_tree()
        load_corpus_tree(["# Two\n## Child\n"])
        second = get_corpus_index()

        assert second is not first
        assert ("Two", "Child") in second.idx_by_path
        assert ("One",) not in second.idx_by_path
        assert second.node_objs[0] is get_corpus_tree()
