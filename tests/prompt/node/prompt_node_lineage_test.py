"""
prompt_node_lineage_test.py

Unit Tests (using pytest) for:

- PromptCorpusNode.generate_id_lineage()
"""

from kaye.gen_prompt import PromptCorpusNode
from tests.prompt import (
    PROMPT1,
    PROMPT3,
)


class TestPrompt1:  ############################################################

    tree = PromptCorpusNode.parse(PROMPT1)

    def test1(_):
        pass


class TestPrompt3:  ############################################################

    tree = PromptCorpusNode.parse(PROMPT3)

    def test1(_):
        pass
