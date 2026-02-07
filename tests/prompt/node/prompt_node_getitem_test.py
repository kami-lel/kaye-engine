"""
prompt_node_getitem_test.py

Unit Tests (using pytest) for:

- PromptCorpusNode.__getitem__()
"""

import pytest

from kaye.gen_prompt import PromptCorpusNode
from tests.prompt import PROMPT3


class TestRoot:

    tree = node = PromptCorpusNode.parse(PROMPT3)

    def test_parent(self):
        with pytest.raises(TypeError) as exec_info:
            self.node[None]

        opt = exec_info.value.args[0]
        assert opt == f"{type(self.node).__name__} index must be int/str: None"

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
        expected = f"index out of range for {str(self.node)}: 99"
        assert opt == expected

    def test_bad_str1(self):
        with pytest.raises(KeyError) as exec_info:
            self.node["???"]

        opt = exec_info.value.args[0]
        expected = f"{str(self.node)} contains no child with name/id of '???'"
        assert opt == expected

    def test_bad_type(self):
        with pytest.raises(TypeError) as exec_info:
            self.node[12.5]

        opt = exec_info.value.args[0]
        expected = f"{type(self.node).__name__} index must be int/str: 12.5"
        assert opt == expected


class TestMain:

    tree = PromptCorpusNode.parse(PROMPT3)
    node = tree.children[0]

    def test_parent(self):
        with pytest.raises(TypeError) as exec_info:
            self.node[None]

        opt = exec_info.value.args[0]
        assert opt == f"{type(self.node).__name__} index must be int/str: None"

    def test_int1(self):
        opt = self.node[0]

        print(opt)

        assert opt is self.tree.children[0].children[0]

    def test_int2(self):
        opt = self.node[1]

        print(opt)

        assert opt is self.tree.children[0].children[1]

    def test_int3(self):
        opt = self.node[2]

        print(opt)

        assert opt is self.tree.children[0].children[2]

    def test_str1(self):
        opt = self.node["Introduction"]

        print(opt)

        assert opt is self.tree.children[0].children[0]

    def test_str2(self):
        opt = self.node["Methods"]

        print(opt)

        assert opt is self.tree.children[0].children[1]

    def test_str3(self):
        opt = self.node["Conclusion"]

        print(opt)

        assert opt is self.tree.children[0].children[2]

    def test_bad_int1(self):
        with pytest.raises(IndexError) as exec_info:
            self.node[99]

        opt = exec_info.value.args[0]
        expected = f"index out of range for {str(self.node)}: 99"
        assert opt == expected

    def test_bad_str1(self):
        with pytest.raises(KeyError) as exec_info:
            self.node["???"]

        opt = exec_info.value.args[0]
        expected = f"{str(self.node)} contains no child with name/id of '???'"
        assert opt == expected

    def test_bad_type(self):
        with pytest.raises(TypeError) as exec_info:
            self.node[12.5]

        opt = exec_info.value.args[0]
        expected = f"{type(self.node).__name__} index must be int/str: 12.5"
        assert opt == expected


class TestImportance:

    tree = PromptCorpusNode.parse(PROMPT3)
    node = tree.children[0].children[0].children[0].children[0]

    def test_parent(self):
        with pytest.raises(TypeError) as exec_info:
            self.node[None]

        opt = exec_info.value.args[0]
        assert opt == f"{type(self.node).__name__} index must be int/str: None"

    def test_int1(self):
        opt = self.node[0]

        print(opt)

        assert (
            opt
            is self.tree.children[0]
            .children[0]
            .children[0]
            .children[0]
            .children[0]
        )

    def test_str1(self):
        opt = self.node["Objective"]

        print(opt)

        assert (
            opt
            is self.tree.children[0]
            .children[0]
            .children[0]
            .children[0]
            .children[0]
        )
