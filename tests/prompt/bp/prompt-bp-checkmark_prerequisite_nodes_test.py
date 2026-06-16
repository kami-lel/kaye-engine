"""
prompt-bp-checkmark_prerequisite_nodes_test.py

Unit Tests (using pytest) for: PromptBlueprint.checkmark_prerequisite_nodes()
"""

import pytest

from kaye.prompt.prompt_corpus_node import PromptCorpusNode
from kaye.prompt.prompt_blueprint import PromptBlueprint


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


class TestCheckmarkPrerequisiteNodes:  #########################################

    def test_parent_unchecked(_, bp_testee):
        bp = bp_testee
        prereq = bp.corpus["Project Title"]["{prerequisite}"]

        bp.checkmark_prerequisite_nodes()

        assert bp.is_checkmarked(prereq) is False

    def test_parent_checked(_, bp_testee):
        bp = bp_testee
        prereq = bp.corpus["Project Title"]["{prerequisite}"]

        bp.checkmark("Project Title")
        bp.checkmark_prerequisite_nodes()

        assert bp.is_checkmarked(prereq) is True

    def test_returns_self(_, bp_testee):
        bp = bp_testee

        opt = bp.checkmark_prerequisite_nodes()

        assert opt is bp
