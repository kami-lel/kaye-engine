"""
prompt-bp-init_test.py

Unit Tests (using pytest) for: PromptBlueprint.__init__()
"""

from kaye.gen_prompt.prompt_bp import PromptBlueprint


class TestEmpty:

    def test_init(_, corpus):
        bp = PromptBlueprint()

        print(bp)

        assert isinstance(bp, dict)
        assert len(bp) == 0
        assert bp.corpus is corpus
        assert isinstance(bp.display_name, str)
        assert bp.display_name == ""


class TestName:

    NAME = "My Blueprint"

    def test_init(self, corpus):
        bp = PromptBlueprint(display_name=self.NAME)

        print(bp)

        assert isinstance(bp, dict)
        assert len(bp) == 0
        assert bp.corpus is corpus
        assert isinstance(bp.display_name, str)
        assert bp.display_name == self.NAME
