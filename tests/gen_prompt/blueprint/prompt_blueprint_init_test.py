"""
prompt_blueprint_init_test.py

Unit Tests (using pytest) for: PromptBlueprint

- .__init__()
- .__repr__()
"""

from kaye.gen_prompt import PromptBlueprint, load_embedded_prompt_corpus

corpus = load_embedded_prompt_corpus()


class TestEmpty:

    def test_init(self):
        bp = PromptBlueprint(corpus)

        print(bp)

        assert isinstance(bp, dict)
        assert len(bp) == 0
        assert bp.corpus is corpus
        assert isinstance(bp.display_name, str)
        assert bp.display_name == ""

    def test_repr(self):
        bp = PromptBlueprint(corpus)

        opt = repr(bp)

        assert opt == "PromptBlueprint()"


class TestName:

    NAME = "My Blueprint"

    def test_init(self):
        bp = PromptBlueprint(corpus, display_name=self.NAME)

        print(bp)

        assert isinstance(bp, dict)
        assert len(bp) == 0
        assert bp.corpus is corpus
        assert isinstance(bp.display_name, str)
        assert bp.display_name == self.NAME

    def test_repr(self):
        bp = PromptBlueprint(corpus, display_name=self.NAME)

        opt = repr(bp)

        assert opt == "PromptBlueprint(My Blueprint)"
