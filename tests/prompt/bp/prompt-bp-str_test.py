"""
prompt-bp-str-test.py

Unit Tests (using pytest) for:

PromptBlueprint.__str__()
"""

from kaye.prompt.prompt_blueprint import PromptBlueprint


class TestEmpty:

    def test_init(_):
        bp = PromptBlueprint()

        opt = str(bp)

        print(opt)
        assert opt == "PromptBlueprint()"


class TestName:

    NAME = "My Blueprint"

    def test_init(self):
        bp = PromptBlueprint(display_name=self.NAME)

        opt = str(bp)

        print(opt)
        assert opt == "PromptBlueprint(My Blueprint)"
