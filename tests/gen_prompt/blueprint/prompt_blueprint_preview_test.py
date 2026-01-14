"""
prompt_blueprint_preview_test.py

Unit Tests (using pytest) for: PromptBlueprint

- .generate_preview_tree()
- .__str__()
"""

from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode
from tests.gen_prompt.node.testees import PROMPT1, PROMPT2

CORPUS1 = PromptCorpusNode.parse(PROMPT1)
CORPUS2 = PromptCorpusNode.parse(PROMPT2)


# test .generate_preview_tree()  ###############################################


# w/ all args
class TestAllArgs1:  # w/ corpus1

    def test_empty(_):
        pass


# no content  ==================================================================

# no comment (nor content)  ====================================================

# full tree (nor content)  =====================================================

# default  =====================================================================

# test __str__()   #############################################################

# TODO TODO
