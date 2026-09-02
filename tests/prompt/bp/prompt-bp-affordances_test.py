"""
prompt-bp-affordances_test.py

Unit Tests (using pytest) for: render_prompt_lines()'s ``variants``
kwarg, auto-checkmarking {variant Usage} sidecars per ``variant_
registry`` entry and {affordance Fallback} sidecars per ``affordance_
registry`` entry
"""

import pytest
from kaye_engine.prompt.affordance_registry import (
    affordance_registry,
    register_variant,
    variant_registry,
)
from kaye_engine.prompt.blueprint.prompt_blueprint import PromptBlueprint
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode


@pytest.fixture
def corpus_with_affordance_sidecars():
    root = PromptCorpusNode("○", None, [])
    section = PromptCorpusNode("Section", root, ["intro"])
    PromptCorpusNode(
        "{[Claude Tool:TestVariant] Usage}", section, ["usage content"]
    )
    PromptCorpusNode(
        "{[Claude Tool:TestFamily] Fallback}", section, ["fallback content"]
    )
    return root


@pytest.fixture
def registered_test_variant():
    entry = register_variant("Claude Tool:TestVariant", "Claude Tool:TestFamily")
    yield entry
    variant_registry.pop(entry.canonical_name, None)
    affordance_registry.pop(entry.affordance_name, None)


@pytest.fixture
def checkmarked_bp(corpus_with_affordance_sidecars):
    bp = PromptBlueprint(corpus_tree=corpus_with_affordance_sidecars)
    bp.checkmark(corpus_with_affordance_sidecars["Section"])
    return bp


@pytest.fixture
def unchecked_bp(corpus_with_affordance_sidecars):
    return PromptBlueprint(corpus_tree=corpus_with_affordance_sidecars)


# Pytest unit tests  ###########################################################
class TestVariantPresent:

    def test_usage_checkmarked_fallback_not(
        _, checkmarked_bp, registered_test_variant
    ):
        opt = checkmarked_bp.generate_prompt_without_dependencies(
            profile=RenderProfile(variants=("Claude Tool:TestVariant",))
        )

        print(opt)
        assert "usage content" in opt
        assert "fallback content" not in opt


class TestVariantAbsent:

    def test_fallback_checkmarked_usage_not(
        _, checkmarked_bp, registered_test_variant
    ):
        opt = checkmarked_bp.generate_prompt_without_dependencies(
            profile=RenderProfile(variants=())
        )

        print(opt)
        assert "fallback content" in opt
        assert "usage content" not in opt


class TestAffordanceWithoutVariants:

    def test_fallback_never_checkmarked(_, checkmarked_bp):
        # no variant registered under "Claude Tool:TestFamily" at all
        opt = checkmarked_bp.generate_prompt_without_dependencies(
            profile=RenderProfile(variants=())
        )

        print(opt)
        assert "fallback content" not in opt


class TestVariantsDisabled:

    def test_neither_checkmarked_when_none(
        _, checkmarked_bp, registered_test_variant
    ):
        opt = checkmarked_bp.generate_prompt_without_dependencies(
            profile=RenderProfile(variants=None)
        )

        print(opt)
        assert "usage content" not in opt
        assert "fallback content" not in opt

    def test_neither_checkmarked_by_default(
        _, checkmarked_bp, registered_test_variant
    ):
        opt = checkmarked_bp.generate_prompt_without_dependencies()

        print(opt)
        assert "usage content" not in opt
        assert "fallback content" not in opt


class TestParentNotCheckmarked:

    def test_neither_spliced_in(_, unchecked_bp, registered_test_variant):
        opt = unchecked_bp.generate_prompt_without_dependencies(
            profile=RenderProfile(variants=("Claude Tool:TestVariant",))
        )

        print(opt)
        assert "usage content" not in opt
        assert "fallback content" not in opt
