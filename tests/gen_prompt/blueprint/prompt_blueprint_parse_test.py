"""
prompt_blueprint_parse_test.py

Unit Tests (using pytest) for: PromptBlueprint.parse()
"""

from kaye.gen_prompt import PromptCorpusNode, PromptBlueprint
from tests.gen_prompt import PROMPT4, PROMPT5

corpus4 = PromptCorpusNode(PROMPT4)
corpus5 = PromptCorpusNode(PROMPT5)

# test by data structure  ######################################################


class TestBasic:

    def test4(_):
        bp_text = """"""

        opt = PromptBlueprint.parse(corpus4, bp_text, disable_prune=True)

        print(opt)

        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 5

        pass


# thorough tests by .generate_preview_tree()  ##################################
# i.e. dep on correct implementation of .generate_preview_tree()

# TODO thorough test after .generate_preview_tree


# Bug tests for errors
