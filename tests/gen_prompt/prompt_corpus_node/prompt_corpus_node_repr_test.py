"""
test ``__repr__()`` of class ``PromptCorpusNode``
"""

from kaye.gen_prompt import PromptCorpusNode
from tests.gen_prompt.prompt_corpus_node.testees import (
    PROMPT1,
    PROMPT2,
    PROMPT3,
)

# TODO


class Test1:  # test using PROMPT1

    tree = PromptCorpusNode.parse(PROMPT1)


class Test2:  # test using PROMPT2

    tree = PromptCorpusNode.parse(PROMPT2)


class Test3:  # test using PROMPT3

    tree = PromptCorpusNode.parse(PROMPT3)
