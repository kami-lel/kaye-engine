"""
prompt-bp-summary_test.py

Unit Tests (using pytest) for:

- show_blueprint()
- BlueprintSummary
"""

import dataclasses

import pytest

from kaye_engine.prompt.blueprint.data import Blueprint, BlueprintMeta
from kaye_engine.prompt.blueprint.summary import (
    BlueprintSummary,
    show_blueprint,
)


class TestShowBlueprint:

    def test_empty_blueprint(_):
        out = show_blueprint(Blueprint())

        assert out == BlueprintSummary(
            meta=BlueprintMeta(),
            node_count=0,
            subtree_count=0,
            dependencies=(),
        )

    def test_counts_nodes_and_subtrees_apart(_):
        bp = Blueprint(
            nodes=frozenset({("A",), ("A", "B")}),
            subtrees=frozenset({("C",)}),
        )

        out = show_blueprint(bp)

        assert (out.node_count, out.subtree_count) == (2, 1)

    def test_carries_meta(_):
        meta = BlueprintMeta(description="what it is")

        assert show_blueprint(Blueprint(meta=meta)).meta == meta

    def test_lists_dependency_names(_):
        bp = Blueprint(dependencies=("x", "y"))

        assert show_blueprint(bp).dependencies == ("x", "y")

    def test_touches_no_corpus(_):
        # meta nodes are only paths: nothing is looked up
        meta = BlueprintMeta(description_node=("Nowhere",))

        assert show_blueprint(Blueprint(meta=meta)).meta == meta


class TestBlueprintSummary:

    def test_is_frozen(_):
        out = show_blueprint(Blueprint())

        with pytest.raises(dataclasses.FrozenInstanceError):
            out.node_count = 5
