"""
prompt_blueprint_remove_test.py

Unit Tests (using pytest) for: PromptBlueprint.remove()
"""

from kaye.gen_prompt import PromptCorpusNode, PromptBlueprint
from tests.gen_prompt import PROMPT1, PROMPT2, PROMPT3
from tests.gen_prompt.blueprint import BLUEPRINT_1_FULL, BLUEPRINT_1_PARTIAL_1

# BUG


class Test1:  # use corpus1  ###################################################

    corpus = PromptCorpusNode.parse(PROMPT1)

    def test1_use_obj1(self):
        bp_text = BLUEPRINT_1_FULL

        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)

        description_node = self.corpus["Project Title"]
        print(opt.keys())

        opt.uncheckmark(description_node)

        print(opt.keys())
        print(opt)
        assert (
            opt.generate_preview_tree(
                preview_line_count=0, hide_comment=True, show_full_tree=True
            )
            == BLUEPRINT_1_PARTIAL_1
        )


class Test2:  # use corpus2  ##############################################

    corpus = PromptCorpusNode.parse(PROMPT2)


class Test3:  # use corpus3  ##############################################

    corpus = PromptCorpusNode.parse(PROMPT3)
