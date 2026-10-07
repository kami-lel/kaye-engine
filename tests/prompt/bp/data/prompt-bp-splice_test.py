"""
prompt-bp-splice_test.py

Unit Tests (using pytest) for:

splice_sidecars
"""

import pytest

from kaye_engine.prompt.affordance_registry import (
    affordance_registry,
    register_variant,
    variant_registry,
)
from kaye_engine.prompt.blueprint.data import Blueprint
from kaye_engine.prompt.blueprint.render.sidecar_splice import splice_sidecars
from kaye_engine.prompt.blueprint.selection import bind_selection
from kaye_engine.prompt.prompt_corpus_loader import load_corpus_tree

_SOURCE = """# Section
intro
## {[Claude Tool:TestVariant] Usage}
usage content
## {[Claude Tool:TestVariant] Lack}
lack content
## {[Claude Tool:TestFamily] Usage}
affordance usage content
## {[Claude Tool:TestFamily] Fallback}
fallback content
## {plain}
plain content
### {nested}
nested content
## Child
# Other
## {plain}
other plain
"""

SECTION = ("Section",)
USAGE = ("Section", "{[Claude Tool:TestVariant] Usage}")
LACK = ("Section", "{[Claude Tool:TestVariant] Lack}")
FAM_USAGE = ("Section", "{[Claude Tool:TestFamily] Usage}")
FALLBACK = ("Section", "{[Claude Tool:TestFamily] Fallback}")
PLAIN = ("Section", "{plain}")
NESTED = ("Section", "{plain}", "{nested}")
OTHER_PLAIN = ("Other", "{plain}")
CHILD = ("Section", "Child")


# pytest fixtures  #############################################################
@pytest.fixture(autouse=True)
def corpus():
    load_corpus_tree([_SOURCE])


@pytest.fixture
def registered_test_variant():
    entry = register_variant(
        "Claude Tool:TestVariant", "Claude Tool:TestFamily"
    )
    yield entry
    variant_registry.pop(entry.canonical_name, None)
    affordance_registry.pop(entry.affordance_name, None)


def _selection(*paths):
    return bind_selection(Blueprint(nodes=frozenset(paths)))


def _bits(selection):
    index = selection.index
    return {
        index.paths[i]
        for i in range(len(index.paths))
        if selection.mask >> i & 1
    }


# pytest  ######################################################################
class TestVariants:

    def test_present(_, registered_test_variant):
        out = splice_sidecars(
            _selection(SECTION),
            conditional_sidecars=(),
            variants=("Claude Tool:TestVariant",),
        )

        assert _bits(out) == {SECTION, USAGE, FAM_USAGE}

    def test_absent(_, registered_test_variant):
        out = splice_sidecars(
            _selection(SECTION), conditional_sidecars=(), variants=()
        )

        assert _bits(out) == {SECTION, LACK, FALLBACK}

    def test_affordance_without_variants_never_spliced(_):
        out = splice_sidecars(
            _selection(SECTION), conditional_sidecars=(), variants=()
        )

        assert _bits(out) == {SECTION}

    def test_disabled_by_none(_, registered_test_variant):
        selection = _selection(SECTION)

        out = splice_sidecars(
            selection, conditional_sidecars=(), variants=None
        )

        assert out is selection

    def test_parent_not_selected(_, registered_test_variant):
        out = splice_sidecars(
            _selection(CHILD), conditional_sidecars=(), variants=()
        )

        assert _bits(out) == {CHILD}


class TestConditionalSidecars:

    def test_named_sidecar_under_selected_parent(_):
        out = splice_sidecars(
            _selection(SECTION),
            conditional_sidecars=("plain",),
            variants=None,
        )

        assert _bits(out) == {SECTION, PLAIN}

    def test_only_sidecars_with_selected_parent(_):
        out = splice_sidecars(
            _selection(SECTION),
            conditional_sidecars=("plain",),
            variants=None,
        )

        assert OTHER_PLAIN not in _bits(out)

    def test_every_matching_parent_is_served(_):
        out = splice_sidecars(
            _selection(SECTION, ("Other",)),
            conditional_sidecars=("plain",),
            variants=None,
        )

        assert {PLAIN, OTHER_PLAIN} <= _bits(out)

    def test_nested_sidecar_follows_spliced_parent(_):
        out = splice_sidecars(
            _selection(SECTION),
            conditional_sidecars=("plain", "nested"),
            variants=None,
        )

        assert NESTED in _bits(out)

    def test_nested_sidecar_alone_needs_its_parent(_):
        out = splice_sidecars(
            _selection(SECTION),
            conditional_sidecars=("nested",),
            variants=None,
        )

        assert NESTED not in _bits(out)

    def test_unknown_name_changes_nothing(_):
        out = splice_sidecars(
            _selection(SECTION),
            conditional_sidecars=("nope",),
            variants=None,
        )

        assert _bits(out) == {SECTION}

    def test_empty_everything_returns_same_selection(_):
        selection = _selection(SECTION)

        assert (
            splice_sidecars(selection, conditional_sidecars=(), variants=None)
            is selection
        )


class TestNoCopy:

    def test_input_selection_untouched(_):
        selection = _selection(SECTION)
        before = selection.mask

        out = splice_sidecars(
            selection, conditional_sidecars=("plain",), variants=None
        )

        assert selection.mask == before
        assert out is not selection
        assert out.index is selection.index
