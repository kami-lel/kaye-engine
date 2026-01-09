"""
prompt_corpus_node_subscript_test.py

Unit Tests (using pytest) for: PromptCorpusNode.__getitem__()
"""

from kaye.gen_prompt import PromptCorpusNode
from tests.gen_prompt.prompt_corpus_node.testees import PROMPT3


class TestRoot:

    def test1(_):
        node = PromptCorpusNode.parse(PROMPT3)

        key = "Introduction"

        # Bug non-functional
        opt = node[key]

        print(opt)
        cf = node[key]
        assert isinstance(opt, PromptCorpusNode)
        assert opt is cf
