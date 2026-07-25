"""
prompt-bp-checkmark_prerequisite_nodes_test.py

Unit Tests (using pytest) for: render.render_prompt_lines(
    bp, contains_sidecars=("prerequisite",)
)
"""

import pytest

from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode
from kaye_engine.prompt.blueprint.prompt_blueprint import PromptBlueprint
from kaye_engine.prompt.blueprint import render


@pytest.fixture
def corpus_with_prerequisite():
    root = PromptCorpusNode("○", None, [])
    proj = PromptCorpusNode("Project Title", root, [])
    PromptCorpusNode("{prerequisite}", proj, ["must finish setup first"])
    PromptCorpusNode("Description", proj, ["blah"])

    return root


@pytest.fixture
def bp_testee(corpus_with_prerequisite):
    return PromptBlueprint.create_empty_blueprint(
        corpus_override=corpus_with_prerequisite
    )


class TestGeneratePromptLinesContainsPrerequisiteNodes:  #################

    def test_parent_unchecked(_, bp_testee):
        bp = bp_testee
        prereq = bp.corpus["Project Title"]["{prerequisite}"]

        lines = render.render_prompt_lines(
            bp, contains_sidecars=("prerequisite",)
        )

        # prerequisite should not be in output if parent is unchecked
        assert prereq.name not in "\n".join(lines)

    def test_parent_checked(_, bp_testee):
        bp = bp_testee
        prereq = bp.corpus["Project Title"]["{prerequisite}"]

        bp.checkmark("Project Title")
        lines = render.render_prompt_lines(
            bp, contains_sidecars=("prerequisite",)
        )

        # prerequisite should be in output if parent is checked
        assert "must finish setup first" in "\n".join(lines)

    def test_without_flag(_, bp_testee):
        bp = bp_testee
        prereq = bp.corpus["Project Title"]["{prerequisite}"]

        bp.checkmark("Project Title")
        lines = render.render_prompt_lines(bp, contains_sidecars=())

        # prerequisite should NOT be in output without the flag
        assert "must finish setup first" not in "\n".join(lines)
