"""
prompt-bp-checkmark_prerequisite_nodes_test.py

Unit Tests (using pytest) for: PromptBlueprint.generate_prompt_lines(
    contains_sidecar_nodes=SidecarNodeType.PREREQUISITE
)
"""

import pytest

from kaye.prompt.prompt_corpus_node import PromptCorpusNode
from kaye.prompt.blueprint.prompt_blueprint import PromptBlueprint
from kaye.prompt.sidecar_nodes import SidecarNodeType


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

        lines = bp.generate_prompt_lines(
            contains_sidecar_nodes=SidecarNodeType.PREREQUISITE
        )

        # prerequisite should not be in output if parent is unchecked
        assert prereq.name not in "\n".join(lines)

    def test_parent_checked(_, bp_testee):
        bp = bp_testee
        prereq = bp.corpus["Project Title"]["{prerequisite}"]

        bp.checkmark("Project Title")
        lines = bp.generate_prompt_lines(
            contains_sidecar_nodes=SidecarNodeType.PREREQUISITE
        )

        # prerequisite should be in output if parent is checked
        assert "must finish setup first" in "\n".join(lines)

    def test_without_flag(_, bp_testee):
        bp = bp_testee
        prereq = bp.corpus["Project Title"]["{prerequisite}"]

        bp.checkmark("Project Title")
        lines = bp.generate_prompt_lines(
            contains_sidecar_nodes=SidecarNodeType.NONE
        )

        # prerequisite should NOT be in output without the flag
        assert "must finish setup first" not in "\n".join(lines)
