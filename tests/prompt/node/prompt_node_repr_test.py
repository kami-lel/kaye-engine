"""
test ``__repr__()`` of class ``PromptCorpusNode``
"""

from kaye.gen_prompt import PromptCorpusNode
from tests.prompt import (
    PROMPT1,
    PROMPT2,
    PROMPT3,
)

# BUG BUG


class Test1:  # test using PROMPT1

    tree = PromptCorpusNode.parse(PROMPT1)

    def test_root(self):
        node = self.tree

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode()"

    def test1(self):
        node = self.tree.children[0]

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title)"

    def test2(self):
        node = self.tree.children[0].children[0]

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#Description)"


class Test2:  # test using PROMPT2

    tree = PromptCorpusNode.parse(PROMPT2)

    def test_root(self):
        node = self.tree

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode()"

    def test1(self):
        node = self.tree.children[0]

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title)"

    def test2(self):
        node = self.tree.children[0].children[0]

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#Description)"

    def test3(self):
        node = self.tree.children[0].children[1]

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#Installation)"

    def test4(self):
        node = self.tree.children[0].children[2]

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#Usage)"

    def test5(self):
        node = self.tree.children[0].children[3]

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#Contributing)"

    def test6(self):
        node = self.tree.children[0].children[4]

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#License)"


class Test3:  # test using PROMPT3

    tree = PromptCorpusNode.parse(PROMPT3)

    def test_root(self):
        node = self.tree

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode()"

    def test1(self):
        node = self.tree.children[0]

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title)"

    def test2(self):
        node = self.tree.children[0].children[0]

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title#Introduction)"

    def test3(self):
        node = self.tree.children[0].children[0].children[0]

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title#Introduction#Background)"

    def test4(self):
        node = self.tree.children[0].children[0].children[0].children[0]

        opt = repr(node)
        print(opt)

        assert (
            opt
            == "PromptCorpusNode(Main Title#Introduction#Background#Importance)"
        )

    def test5(self):
        node = (
            self.tree.children[0]
            .children[0]
            .children[0]
            .children[0]
            .children[0]
        )

        opt = repr(node)
        print(opt)

        assert (
            opt
            == "PromptCorpusNode"
            "(Main Title#Introduction#Background#Importance#Objective)"
        )

    def test21(self):
        node = self.tree.children[0].children[1]

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title#Methods)"

    def test22(self):
        node = self.tree.children[0].children[1].children[0]

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title#Methods#Data Collection)"

    def test23(self):
        node = self.tree.children[0].children[1].children[0].children[0]

        opt = repr(node)
        print(opt)

        assert (
            opt
            == "PromptCorpusNode(Main Title#Methods#Data Collection#Tools Used)"
        )

    def test24(self):
        node = (
            self.tree.children[0]
            .children[1]
            .children[0]
            .children[0]
            .children[0]
        )

        opt = repr(node)
        print(opt)

        assert (
            opt
            == "PromptCorpusNode"
            "(Main Title#Methods#Data Collection#Tools Used#Future Work)"
        )

    def test31(self):
        node = self.tree.children[0].children[2]

        opt = repr(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title#Conclusion)"
