"""
prompt_blueprint_parse_test.py

Unit Tests (using pytest) for: PromptBlueprint.parse()
"""

from kaye.gen_prompt import PromptCorpusNode, PromptBlueprint
from testees import PROMPT1, PROMPT2

corpus1 = PromptCorpusNode(PROMPT1)
corpus2 = PromptCorpusNode(PROMPT2)

# test by data structure  ######################################################


class TestBasic:

    def test1(_):
        bp_text = """"""

        opt = PromptBlueprint.parse(corpus1, bp_text, disable_prune=True)

        print(opt)

        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 5

        pass


# thorough tests by .generate_preview_tree()  ##################################
# i.e. dep on correct implementation of .generate_preview_tree()

# TODO thorough test after .generate_preview_tree


# Bug tests for errors
