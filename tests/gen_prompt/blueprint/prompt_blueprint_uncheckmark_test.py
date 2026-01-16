"""
prompt_blueprint_uncheckmark_test.py

Unit Tests (using pytest) for: PromptBlueprint.remove()
"""

from math import floor, ceil

from kaye.gen_prompt import PromptCorpusNode, PromptBlueprint
from tests.gen_prompt import PROMPT1, PROMPT2, PROMPT3
from tests.gen_prompt.blueprint import BLUEPRINT_1_FULL, BLUEPRINT_1_PARTIAL_1


class Test1:  # use corpus1  ###################################################

    corpus = PromptCorpusNode.parse(PROMPT1)

    # full -> partial 1  -------------------------------------------------------
    def test1_use_obj(self):
        bp_text = BLUEPRINT_1_FULL

        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_title("before uncheckmark")

        description_node = self.corpus["Project Title"]

        _print_title("after uncheckmark")
        ret = opt.uncheckmark(description_node)
        print(opt)

        _print_title("returned object")
        print(ret)

        assert (
            opt.generate_preview_tree(
                preview_line_count=0, hide_comment=True, show_full_tree=True
            )
            == BLUEPRINT_1_PARTIAL_1
        )

        assert (
            ret.generate_preview_tree(
                preview_line_count=0, hide_comment=True, show_full_tree=True
            )
            == BLUEPRINT_1_PARTIAL_1
        )

    # full -> partial 2  -------------------------------------------------------
    # TODO more tests


class Test2:  # use corpus2  ##############################################

    corpus = PromptCorpusNode.parse(PROMPT2)

    # full -> partial 1  -------------------------------------------------------


class Test3:  # use corpus3  ##############################################

    corpus = PromptCorpusNode.parse(PROMPT3)

    # full -> partial 1  -------------------------------------------------------
    # full -> partial 2  -------------------------------------------------------


# helper  ######################################################################


def _print_title(content):
    filler_length = (76 - len(content)) / 2
    FILLER = "#"
    print(
        FILLER * ceil(filler_length) + content + FILLER * floor(filler_length)
    )
