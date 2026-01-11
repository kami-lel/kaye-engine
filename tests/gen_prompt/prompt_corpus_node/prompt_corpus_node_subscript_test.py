"""
prompt_corpus_node_subscript_test.py

Unit Tests (using pytest) for: PromptCorpusNode.__getitem__()
"""

import pytest

from kaye.gen_prompt import PromptCorpusNode
from tests.gen_prompt.prompt_corpus_node.testees import PROMPT3


class TestRoot:

    tree = node = PromptCorpusNode.parse(PROMPT3)

    def test_parent(self):
        opt = self.node[None]

        print(opt)

        assert opt is None

    def test_int1(self):
        opt = self.node[0]

        print(opt)

        assert opt is self.tree.children[0]

    def test_str1(self):
        opt = self.node["Main Title"]

        print(opt)

        assert opt is self.tree.children[0]

    def test_bad_int1(self):
        with pytest.raises(IndexError) as exec_info:
            self.node[99]

        opt = exec_info.value.args[0]
        assert opt == "index out of range for PromptCorpusNode children: 99"

    def test_bad_str1(self):
        with pytest.raises(KeyError) as exec_info:
            self.node["???"]

        opt = exec_info.value.args[0]
        assert opt == "fail to find child '???' in this PromptCorpusNode"

    def test_bad_type(self):
        with pytest.raises(TypeError) as exec_info:
            self.node[12.5]

        opt = exec_info.value.args[0]
        assert (
            opt == "unsupported type for PromptCorpusNode[~]: <class 'float'>"
        )
