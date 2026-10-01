"""
prompt-index-blocks_test.py

Unit Tests (using pytest) for:

CorpusIndex.blocks, CorpusIndex.sidecar_masks, get_corpus_node,
BlueprintSelection
"""

import pytest

from kaye_engine.prompt.blueprint.index import (
    BlueprintSelection,
    get_corpus_index,
    get_corpus_node,
)
from kaye_engine.prompt.dynamic_nodes import TodayNode
from kaye_engine.prompt.dynamic_nodes.dynamic_node import DynamicNode
from kaye_engine.prompt.prompt_corpus_loader import load_corpus_tree

_SOURCE = """# A
A body.
more.
## B
## {description}
Does things.
## {avoid}
Nothing bad.
# C
## {avoid}
Other.
"""


# pytest fixtures  #############################################################
@pytest.fixture
def index():
    load_corpus_tree([_SOURCE])
    return get_corpus_index()


# pytest  ######################################################################
class TestBlocks:

    def test_equal_old_walk_per_node(_, index):
        for node, block in zip(index.node_objs, index.blocks):
            if isinstance(node, DynamicNode):
                continue
            expected = ["#" * node.depth + " " + node.name]
            expected.extend(node.content_lines())
            assert list(block) == expected

    def test_heading_and_content(_, index):
        block = index.blocks[index.idx_by_path[("A",)]]

        assert block == ("# A", "A body.", "more.")

    def test_empty_content_is_heading_only(_, index):
        block = index.blocks[index.idx_by_path[("A", "B")]]

        assert block == ("## B",)

    def test_dynamic_node_is_none(_, index):
        idx = next(
            i for i, n in enumerate(index.node_objs) if isinstance(n, TodayNode)
        )

        assert index.blocks[idx] is None

    def test_every_dynamic_node_is_none_and_no_other(_, index):
        for node, block in zip(index.node_objs, index.blocks):
            assert (block is None) == isinstance(node, DynamicNode)


class TestSidecarMasks:

    def test_names_and_bits(_, index):
        masks = index.sidecar_masks

        assert set(masks) == {"description", "avoid"}
        assert masks["description"] == 1 << index.idx_by_path[
            ("A", "{description}")
        ]

    def test_same_name_collects_every_node(_, index):
        expected = (1 << index.idx_by_path[("A", "{avoid}")]) | (
            1 << index.idx_by_path[("C", "{avoid}")]
        )

        assert index.sidecar_masks["avoid"] == expected

    def test_non_sidecar_absent(_, index):
        every = 0
        for mask in index.sidecar_masks.values():
            every |= mask

        assert every & (1 << index.idx_by_path[("A",)]) == 0


class TestGetCorpusNode:

    def test_finds_node(_, index):
        node = get_corpus_node("A", "B")

        assert node.name == "B"
        assert node is index.node_objs[index.idx_by_path[("A", "B")]]

    def test_root_for_empty_path(_, index):
        assert get_corpus_node() is index.node_objs[0]

    def test_unknown_path_raises_naming_it(_, index):
        with pytest.raises(ValueError, match="Nope"):
            get_corpus_node("A", "Nope")


class TestBlueprintSelection:

    def test_holds_index_and_mask(_, index):
        selection = BlueprintSelection(index, 0b101)

        assert selection.index is index
        assert selection.mask == 0b101
        assert selection == BlueprintSelection(index, 0b101)
