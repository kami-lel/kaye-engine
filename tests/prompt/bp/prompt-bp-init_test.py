"""
prompt-bp-init_test.py

Unit Tests (using pytest) for: PromptBlueprint.__init__()
"""

import pytest

from kaye.prompt.blueprint.prompt_blueprint import (
    PromptBlueprint,
    load_prompt_corpus_tree,
)


class TestEmpty:

    def test_init(_, corpus):
        bp = PromptBlueprint()

        print(bp)

        assert isinstance(bp, dict)
        assert len(bp) == 0
        assert bp.corpus == corpus
        assert isinstance(bp.display_name, str)
        assert bp.display_name == ""


class TestName:

    NAME = "My Blueprint"

    def test_init(self, corpus):
        bp = PromptBlueprint(display_name=self.NAME)

        print(bp)

        assert isinstance(bp, dict)
        assert len(bp) == 0
        assert bp.corpus == corpus
        assert isinstance(bp.display_name, str)
        assert bp.display_name == self.NAME


class TestErr:

    def test1(_):
        corpus_override = 123

        with pytest.raises(ValueError) as exec_info:
            PromptBlueprint(corpus_override=corpus_override)
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "kwarg corpus_override must be a root node: 123"

    def test2(_):
        node = load_prompt_corpus_tree()[0]

        with pytest.raises(ValueError) as exec_info:
            PromptBlueprint(corpus_override=node)
        opt = exec_info.value.args[0]

        print(opt)
        assert (
            opt
            == "kwarg corpus_override must be a root node: "
            "PromptCorpusNode(Introduction)"
        )
