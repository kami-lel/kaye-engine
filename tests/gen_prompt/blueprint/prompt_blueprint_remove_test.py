"""
prompt_blueprint_remove_test.py

Unit Tests (using pytest) for: PromptBlueprint.remove()
"""

from kaye.gen_prompt import PromptCorpusNode, PromptBlueprint
from tests.gen_prompt import PROMPT1, PROMPT2, PROMPT3
from tests.gen_prompt.blueprint import (
    BLUEPRINT_1_FULL,
)

# TODO


class Test1:  # use corpus1  ###################################################

    corpus = PromptCorpusNode.parse(PROMPT1)

    def test_obj1(self):
        bp_text = BLUEPRINT_1_FULL

        bp = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)


class Test2:  # use corpus2  ##############################################

    corpus = PromptCorpusNode.parse(PROMPT2)


class Test3:  # use corpus3  ##############################################

    corpus = PromptCorpusNode.parse(PROMPT3)
