"""
prompt-bp-str-test.py

Unit Tests (using pytest) for:

PromptBlueprint.__str__()
"""

from kaye.prompt.blueprint.prompt_blueprint import PromptBlueprint


class TestEmpty:

    def test_init(_):
        bp = PromptBlueprint()

        opt = str(bp)

        print(opt)
        # str() has no dedicated override; falls back to __repr__(), the
        # tree-preview dump
        assert opt == repr(bp)
        assert opt == bp.generate_blueprint()
