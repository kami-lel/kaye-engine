"""
prompt-node-copy-test.py

Unit Tests (using pytest) for:

copy & deepcopy of PromptCorpusNode
"""

import copy


import pytest


# fixtures  ####################################################################
@pytest.fixture
def copy_testee1(corpus_testee1):
    return copy.copy(corpus_testee1)


@pytest.fixture
def deepcopy_testee1(corpus_testee1):
    return copy.deepcopy(corpus_testee1)


@pytest.fixture
def copy_testee3(corpus_testee3):
    return copy.copy(corpus_testee3)


@pytest.fixture
def deepcopy_testee3(corpus_testee3):
    return copy.deepcopy(corpus_testee3)


class TestPrompt1:  ############################################################

    def test_root(_, corpus_testee1):
        src_node = corpus_testee1

        opt = copy.copy(src_node)
        print(str(opt))

        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

        assert len(src_node.descendants) == 4

    def test_project(_, corpus_testee1):
        tree = corpus_testee1
        src_node = tree.children[0]

        opt = copy.copy(src_node)

        print(str(opt))
        assert src_node.name == opt.name
        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

        assert len(src_node.descendants) == 3

    def test_sub1(_, corpus_testee1):
        tree = corpus_testee1
        project = tree.children[0]
        src_node = project.children[0]

        opt = copy.copy(src_node)

        print(str(opt))
        assert src_node.name == opt.name
        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

        assert len(src_node.descendants) == 0

    # deepcopy  ================================================================

    def test_deepcopy1(_, corpus_testee1, deepcopy_testee1):
        copied = deepcopy_testee1
        src = corpus_testee1

        print(copied.generate_prompt_tree_preview(content_preview_lines=0))

        assert copied.name == "○"
        assert copied._content_lines == src._content_lines
        assert len(copied.descendants) == len(src.descendants)

        # BUG copy/deepcopy will modify root node
        assert len(src.descendants) == 4

    def test_deepcopy2(_, corpus_testee1, deepcopy_testee1):
        copied = deepcopy_testee1.children[0].children[1]
        src = corpus_testee1.children[0].children[1]

        assert copied.name == src.name
        assert copied._content_lines == src._content_lines
        assert len(copied.descendants) == len(src.descendants)


class TestPrompt2:  ############################################################
    def test_root(_, corpus_testee2):
        src_node = corpus_testee2

        opt = copy.copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_project(_, corpus_testee2):
        tree = corpus_testee2
        src_node = tree.children[0]

        opt = copy.copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_description(_, corpus_testee2):
        tree = corpus_testee2
        project = tree.children[0]
        src_node = project.children[0]

        opt = copy.copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_install(_, corpus_testee2):
        tree = corpus_testee2
        project = tree.children[0]
        src_node = project.children[1]

        opt = copy.copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_usage1(_, corpus_testee2):
        tree = corpus_testee2
        project = tree.children[0]
        src_node = project.children[2]

        opt = copy.copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines


class TestPrompt3:  ############################################################

    def test_root(_, corpus_testee3):
        src_node = corpus_testee3

        opt = copy.copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

        assert len(src_node.descendants) == 10

    def test_project(_, corpus_testee3):
        tree = corpus_testee3
        src_node = tree.children[0]

        opt = copy.copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_intro(_, corpus_testee3):
        tree = corpus_testee3
        project = tree.children[0]
        src_node = project.children[0]

        opt = copy.copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_intro_bg(_, corpus_testee3):
        tree = corpus_testee3
        project = tree.children[0]
        parent = project.children[0]
        src_node = parent.children[0]

        opt = copy.copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_intro_bg_mpt(_, corpus_testee3):
        tree = corpus_testee3
        project = tree.children[0]
        parent = project.children[0].children[0]
        src_node = parent.children[0]

        opt = copy.copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_intro_bg_mpt_obj(_, corpus_testee3):
        tree = corpus_testee3
        project = tree.children[0]
        parent = project.children[0].children[0].children[0]
        src_node = parent.children[0]

        opt = copy.copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    # deepcopy  ================================================================

    def test_deepcopy1(_, corpus_testee3, deepcopy_testee3):
        copied = deepcopy_testee3
        src = corpus_testee3

        print(copied.generate_prompt_tree_preview(content_preview_lines=0))

        assert copied.name == "○"
        assert copied._content_lines == src._content_lines
        assert len(copied.descendants) == len(src.descendants)

        # BUG copy/deepcopy will modify root node
        assert len(src.descendants) == 10

    def test_deepcopy2(_, corpus_testee3, deepcopy_testee3):
        copied = deepcopy_testee3.children[0].children[1]
        src = corpus_testee3.children[0].children[1]

        assert copied.name == src.name
        assert copied._content_lines == src._content_lines
        assert len(copied.descendants) == len(src.descendants)

    def test_deepcopy3(_, corpus_testee3, deepcopy_testee3):
        copied = (
            deepcopy_testee3.children[0].children[1].children[0].children[0]
        )
        src = corpus_testee3.children[0].children[1].children[0].children[0]

        assert copied.name == src.name
        assert copied._content_lines == src._content_lines
        assert len(copied.descendants) == len(src.descendants)
