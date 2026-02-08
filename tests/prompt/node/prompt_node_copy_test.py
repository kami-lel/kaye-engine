"""
prompt_corpus_node_copy_test.py

Unit XXTests (using pytest) for: PromptCorpusNode.__copy__()
"""

from copy import copy

from kaye.gen_prompt import PromptCorpusNode
from tests.prompt import (
    PROMPT1,
    PROMPT2,
    PROMPT3,
)

# BUG rm or make possible


class XTestParse1:  # test using PROMPT1

    def test_root(self):
        src_node = PromptCorpusNode.parse(PROMPT1)

        opt = copy(src_node)
        print(str(opt))

        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node.content == opt.content

    def test_project(self):
        tree = PromptCorpusNode.parse(PROMPT1)
        src_node = tree.children[0]

        opt = copy(src_node)

        print(str(opt))
        assert src_node.name == opt.name
        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node.content == opt.content

    def test_sub1(self):
        tree = PromptCorpusNode.parse(PROMPT1)
        project = tree.children[0]
        src_node = project.children[0]

        opt = copy(src_node)

        print(str(opt))
        assert src_node.name == opt.name
        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node.content == opt.content


class XTestParse2:  # test using PROMPT2

    def test_root(self):
        src_node = PromptCorpusNode.parse(PROMPT2)

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node.content == opt.content

    def test_project(self):
        tree = PromptCorpusNode.parse(PROMPT2)
        src_node = tree.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node.content == opt.content

    def test_description(self):
        tree = PromptCorpusNode.parse(PROMPT2)
        project = tree.children[0]
        src_node = project.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node.content == opt.content

    def test_install(self):
        tree = PromptCorpusNode.parse(PROMPT2)
        project = tree.children[0]
        src_node = project.children[1]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node.content == opt.content

    def test_usage1(self):
        tree = PromptCorpusNode.parse(PROMPT2)
        project = tree.children[0]
        src_node = project.children[2]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node.content == opt.content


class XTestParse3:  # test using PROMPT3

    def test_root(self):
        src_node = PromptCorpusNode.parse(PROMPT3)

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node.content == opt.content

    def test_project(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        src_node = tree.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node.content == opt.content

    def test_intro(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        src_node = project.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node.content == opt.content

    def test_intro_bg(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[0]
        src_node = parent.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node.content == opt.content

    def test_intro_bg_mpt(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[0].children[0]
        src_node = parent.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node.content == opt.content

    def test_intro_bg_mpt_obj(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[0].children[0].children[0]
        src_node = parent.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node.content == opt.content
