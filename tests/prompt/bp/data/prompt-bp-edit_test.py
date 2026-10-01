"""
prompt-bp-edit_test.py

Unit Tests (using pytest) for:

checkmark_nodes, uncheckmark_nodes, is_checkmarked, merge_blueprints,
replace_meta, create_blueprint_from_node
"""

import pytest

from kaye_engine.prompt.blueprint.data import (
    Blueprint,
    BlueprintMeta,
    create_blueprint,
)
from kaye_engine.prompt.blueprint.edit import (
    checkmark_nodes,
    create_blueprint_from_node,
    is_checkmarked,
    merge_blueprints,
    replace_meta,
    uncheckmark_nodes,
)
from kaye_engine.prompt.blueprint.index import get_corpus_node
from kaye_engine.prompt.prompt_corpus_loader import (
    clear_corpus_tree,
    load_corpus_tree,
)

_SOURCE = """# Main
## Intro
### Background
#### Importance
## Methods
### Data
### {globs}
```glob
*.py
```
# Conclusion
"""

A = ("Main",)
INTRO = ("Main", "Intro")
BACK = ("Main", "Intro", "Background")
IMPORTANCE = ("Main", "Intro", "Background", "Importance")
METHODS = ("Main", "Methods")
DATA = ("Main", "Methods", "Data")
GLOBS = ("Main", "Methods", "{globs}")
CONCLUSION = ("Conclusion",)


# pytest fixtures  #############################################################
@pytest.fixture(autouse=True)
def corpus():
    load_corpus_tree([_SOURCE])


# pytest  ######################################################################
class TestCheckmark:

    def test_by_path(_):
        bp = checkmark_nodes(create_blueprint(), INTRO)

        assert bp.nodes == {INTRO}
        assert is_checkmarked(bp, INTRO)
        assert not is_checkmarked(bp, BACK)

    def test_by_name_and_object(_):
        bp = checkmark_nodes(create_blueprint(), "Intro")
        bp = checkmark_nodes(bp, get_corpus_node(*METHODS))

        assert bp.nodes == {INTRO, METHODS}

    def test_returns_new_blueprint(_):
        before = create_blueprint()

        after = checkmark_nodes(before, INTRO)

        assert before.nodes == frozenset()
        assert after is not before

    def test_idempotent(_):
        once = checkmark_nodes(create_blueprint(), INTRO)

        assert checkmark_nodes(once, INTRO) == once

    def test_recursive_records_subtree(_):
        bp = checkmark_nodes(create_blueprint(), INTRO, is_recursive=True)

        assert bp.subtrees == {INTRO}
        assert bp.nodes == frozenset()
        assert is_checkmarked(bp, IMPORTANCE)

    def test_recursive_skips_sidecars(_):
        bp = checkmark_nodes(create_blueprint(), METHODS, is_recursive=True)

        assert is_checkmarked(bp, DATA)
        assert not is_checkmarked(bp, GLOBS)

    def test_explicit_sidecar(_):
        bp = checkmark_nodes(create_blueprint(), GLOBS)

        assert is_checkmarked(bp, GLOBS)

    def test_dynamic_node(_):
        bp = checkmark_nodes(create_blueprint(), "(today)")

        assert is_checkmarked(bp, "(today)")

    @pytest.mark.parametrize(
        "bad, error",
        [
            ("Nope", ValueError),
            (("Main", "Nope"), ValueError),
            (12345, TypeError),
            (None, TypeError),
            (["Main"], TypeError),
        ],
    )
    def test_bad_argument(_, bad, error):
        with pytest.raises(error):
            checkmark_nodes(create_blueprint(), bad)

    def test_unknown_path_named_in_error(_):
        with pytest.raises(ValueError, match="Nope"):
            checkmark_nodes(create_blueprint(), ("Main", "Nope"))

    def test_node_of_another_tree_rejected(_):
        node = get_corpus_node(*INTRO)
        clear_corpus_tree()
        load_corpus_tree([_SOURCE])

        with pytest.raises(ValueError, match="does not belong"):
            checkmark_nodes(create_blueprint(), node)


class TestUncheckmark:

    def test_removes_node_only(_):
        bp = checkmark_nodes(checkmark_nodes(create_blueprint(), INTRO), BACK)

        bp = uncheckmark_nodes(bp, INTRO)

        assert bp.nodes == {BACK}

    def test_unchecked_is_noop(_):
        bp = checkmark_nodes(create_blueprint(), INTRO)

        assert uncheckmark_nodes(bp, METHODS) == bp
        assert uncheckmark_nodes(create_blueprint(), METHODS) == (
            create_blueprint()
        )

    def test_covered_node_expands_subtree(_):
        bp = checkmark_nodes(create_blueprint(), A, is_recursive=True)

        bp = uncheckmark_nodes(bp, INTRO)

        assert bp.subtrees == frozenset()
        assert not is_checkmarked(bp, INTRO)
        for kept in (A, BACK, IMPORTANCE, METHODS, DATA):
            assert is_checkmarked(bp, kept)
        assert not is_checkmarked(bp, GLOBS)
        assert not is_checkmarked(bp, CONCLUSION)

    def test_recursive_removes_beneath(_):
        bp = create_blueprint()
        for path in (INTRO, BACK, METHODS):
            bp = checkmark_nodes(bp, path)
        bp = checkmark_nodes(bp, IMPORTANCE, is_recursive=True)

        bp = uncheckmark_nodes(bp, INTRO, is_recursive=True)

        assert bp.nodes == {METHODS}
        assert bp.subtrees == frozenset()

    def test_recursive_inside_covering_subtree(_):
        bp = checkmark_nodes(create_blueprint(), A, is_recursive=True)

        bp = uncheckmark_nodes(bp, INTRO, is_recursive=True)

        for gone in (INTRO, BACK, IMPORTANCE):
            assert not is_checkmarked(bp, gone)
        for kept in (A, METHODS, DATA):
            assert is_checkmarked(bp, kept)

    def test_recursive_removes_own_subtree_entry(_):
        bp = checkmark_nodes(create_blueprint(), INTRO, is_recursive=True)

        assert uncheckmark_nodes(bp, INTRO, is_recursive=True) == (
            create_blueprint()
        )

    def test_sidecar_under_subtree_is_unchecked_noop(_):
        bp = checkmark_nodes(create_blueprint(), METHODS, is_recursive=True)

        assert uncheckmark_nodes(bp, GLOBS) == bp

    def test_bad_argument(_):
        with pytest.raises(ValueError):
            uncheckmark_nodes(create_blueprint(), "Nope")


class TestMerge:

    def test_union(_):
        left = checkmark_nodes(create_blueprint(), INTRO)
        right = checkmark_nodes(create_blueprint(), METHODS)
        right = checkmark_nodes(right, CONCLUSION, is_recursive=True)

        merged = merge_blueprints(left, right)

        assert merged.nodes == {INTRO, METHODS}
        assert merged.subtrees == {CONCLUSION}

    def test_commutative_in_selection(_):
        left = checkmark_nodes(create_blueprint(), INTRO)
        right = checkmark_nodes(create_blueprint(), METHODS)

        assert merge_blueprints(left, right).nodes == (
            merge_blueprints(right, left).nodes
        )

    def test_meta_left_priority(_):
        left = Blueprint(meta=BlueprintMeta(description="left"))
        right = Blueprint(
            meta=BlueprintMeta(description="right", globs_node=GLOBS)
        )

        merged = merge_blueprints(left, right)

        assert merged.meta.description == "left"
        assert merged.meta.globs_node == GLOBS

    def test_dependencies_deduplicated_in_order(_):
        left = create_blueprint(dependencies=["a", "b"])
        right = create_blueprint(dependencies=["b", "c"])

        assert merge_blueprints(left, right).dependencies == ("a", "b", "c")

    def test_no_corpus_mismatch_possible(_):
        # a blueprint holds no corpus, so merging cannot fail on one
        assert merge_blueprints(create_blueprint(), create_blueprint()) == (
            create_blueprint()
        )


class TestReplaceMeta:

    def test_literal_description(_):
        bp = replace_meta(create_blueprint(), description="Hello")

        assert bp.meta.description == "Hello"

    def test_node_fields_normalized_to_paths(_):
        bp = replace_meta(
            create_blueprint(),
            globs_node=get_corpus_node(*GLOBS),
            description_node="Intro",
        )

        assert bp.meta.globs_node == GLOBS
        assert bp.meta.description_node == INTRO

    def test_none_clears(_):
        bp = replace_meta(create_blueprint(), description="x")

        assert replace_meta(bp, description=None).meta.description is None

    def test_other_fields_kept(_):
        bp = replace_meta(create_blueprint(), description="x")
        bp = replace_meta(bp, globs_node=GLOBS)

        assert bp.meta.description == "x"

    def test_unknown_field(_):
        with pytest.raises(TypeError):
            replace_meta(create_blueprint(), nonsense=1)

    def test_unknown_node(_):
        with pytest.raises(ValueError):
            replace_meta(create_blueprint(), globs_node="Nope")


class TestCreateFromNode:

    def test_single_node(_):
        bp = create_blueprint_from_node(get_corpus_node(*INTRO))

        assert bp.nodes == {INTRO}

    def test_recursive(_):
        bp = create_blueprint_from_node("Intro", is_recursive=True)

        assert bp.subtrees == {INTRO}

    def test_keeps_dependencies_and_meta(_):
        bp = create_blueprint_from_node(
            INTRO,
            dependencies=["coder"],
            meta=BlueprintMeta(description="d"),
        )

        assert bp.dependencies == ("coder",)
        assert bp.meta.description == "d"
