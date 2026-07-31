"""
prompt-bp-init_test.py

Unit Tests (using pytest) for: PromptBlueprint.__init__()
"""

import pytest

from kaye_engine.prompt.blueprint.prompt_blueprint import PromptBlueprint


class TestEmpty:

    def test_init(_, corpus):
        bp = PromptBlueprint()

        print(bp)

        assert isinstance(bp, dict)
        assert len(bp) == 0
        assert bp.corpus == corpus


class TestErr:

    def test1(_):
        corpus_tree = 123

        with pytest.raises(ValueError) as exec_info:
            PromptBlueprint(corpus_tree=corpus_tree)
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == (
            "corpus_tree must be a root node or a registered tree name: 123"
        )

    def test2(_, corpus):
        node = corpus[0]

        with pytest.raises(ValueError) as exec_info:
            PromptBlueprint(corpus_tree=node)
        opt = exec_info.value.args[0]

        print(opt)
        assert (
            opt
            == "corpus_tree must be a root node or a registered tree name: "
            "PromptCorpusNode(Project Title)"
        )
