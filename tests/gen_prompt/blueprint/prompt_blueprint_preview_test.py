"""
prompt_blueprint_preview_test.py

Unit Tests (using pytest) for: PromptBlueprint

- .generate_preview_tree()
- .__str__()
"""

from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode
from tests.gen_prompt.node.testees import PROMPT1, PROMPT2

corpus1 = PromptCorpusNode.parse(PROMPT1)
corpus2 = PromptCorpusNode.parse(PROMPT2)


# test .generate_preview_tree()  ###############################################
class TestAllArgs1:  # test w/ all args with PROMPT1

    def test_empty(_):
        pass


# no content  ==================================================================

# no comment (nor content)  ====================================================

# full tree (nor content)  =====================================================

# default  =====================================================================

# test __str__()   #############################################################

# TODO TODO
