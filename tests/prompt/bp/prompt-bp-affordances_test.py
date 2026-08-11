"""
prompt-bp-affordances_test.py

Unit Tests (using pytest) for: render_prompt_lines()'s ``affordances``
kwarg, auto-checkmarking {name Usage}/{name Lack} sidecars registered
in ``affordance_registry``
"""

import pytest

from kaye_engine.prompt.affordance_registry import (
    affordance_registry,
    register_affordance,
)
from kaye_engine.prompt.blueprint.prompt_blueprint import PromptBlueprint
from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode


@pytest.fixture
def corpus_with_affordance_sidecars():
    root = PromptCorpusNode("○", None, [])
    section = PromptCorpusNode("Section", root, ["intro"])
    PromptCorpusNode(
        "{[Claude Tool:TestAff] Usage}", section, ["usage content"]
    )
    PromptCorpusNode("{[Claude Tool:TestAff] Lack}", section, ["lack content"])
    return root


@pytest.fixture
def registered_test_affordance():
    entry = register_affordance("Claude Tool:TestAff", "TestAff")
    yield entry
    affordance_registry.pop(entry.canonical_name, None)


@pytest.fixture
def checkmarked_bp(corpus_with_affordance_sidecars):
    bp = PromptBlueprint(corpus_tree=corpus_with_affordance_sidecars)
    bp.checkmark(corpus_with_affordance_sidecars["Section"])
    return bp


@pytest.fixture
def unchecked_bp(corpus_with_affordance_sidecars):
    return PromptBlueprint(corpus_tree=corpus_with_affordance_sidecars)


class TestAffordancePresent:  #######################################################

    def test_usage_checkmarked_lack_not(
        _, checkmarked_bp, registered_test_affordance
    ):
        opt = checkmarked_bp.generate_prompt(
            affordances=("Claude Tool:TestAff",)
        )

        print(opt)
        assert "usage content" in opt
        assert "lack content" not in opt


class TestAffordanceAbsent:  ########################################################

    def test_lack_checkmarked_usage_not(
        _, checkmarked_bp, registered_test_affordance
    ):
        opt = checkmarked_bp.generate_prompt(affordances=())

        print(opt)
        assert "lack content" in opt
        assert "usage content" not in opt


class TestAffordancesDisabled:  #####################################################

    def test_neither_checkmarked_when_none(
        _, checkmarked_bp, registered_test_affordance
    ):
        opt = checkmarked_bp.generate_prompt(affordances=None)

        print(opt)
        assert "usage content" not in opt
        assert "lack content" not in opt

    def test_neither_checkmarked_by_default(
        _, checkmarked_bp, registered_test_affordance
    ):
        opt = checkmarked_bp.generate_prompt()

        print(opt)
        assert "usage content" not in opt
        assert "lack content" not in opt


class TestParentNotCheckmarked:  ####################################################

    def test_neither_spliced_in(_, unchecked_bp, registered_test_affordance):
        opt = unchecked_bp.generate_prompt(
            affordances=("Claude Tool:TestAff",)
        )

        print(opt)
        assert "usage content" not in opt
        assert "lack content" not in opt
