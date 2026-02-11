"""
prompt-bp-copy_test.py

Unit Tests (using pytest) for: PromptCorpusNode.__copy__()
"""

from copy import copy


class TestParse1:  #############################################################

    def test_root(_, corpus_testee1):
        src_node = corpus_testee1

        opt = copy(src_node)
        print(str(opt))

        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_project(_, corpus_testee1):
        tree = corpus_testee1
        src_node = tree.children[0]

        opt = copy(src_node)

        print(str(opt))
        assert src_node.name == opt.name
        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_sub1(_, corpus_testee1):
        tree = corpus_testee1
        project = tree.children[0]
        src_node = project.children[0]

        opt = copy(src_node)

        print(str(opt))
        assert src_node.name == opt.name
        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines


class TestParse2:  #############################################################
    def test_root(_, corpus_testee2):
        src_node = corpus_testee2

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_project(_, corpus_testee2):
        tree = corpus_testee2
        src_node = tree.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_description(_, corpus_testee2):
        tree = corpus_testee2
        project = tree.children[0]
        src_node = project.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_install(_, corpus_testee2):
        tree = corpus_testee2
        project = tree.children[0]
        src_node = project.children[1]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_usage1(_, corpus_testee2):
        tree = corpus_testee2
        project = tree.children[0]
        src_node = project.children[2]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines


class TestParse3:  #############################################################

    def test_root(_, corpus_testee3):
        src_node = corpus_testee3

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_project(_, corpus_testee3):
        tree = corpus_testee3
        src_node = tree.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_intro(_, corpus_testee3):
        tree = corpus_testee3
        project = tree.children[0]
        src_node = project.children[0]

        opt = copy(src_node)
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

        opt = copy(src_node)
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

        opt = copy(src_node)
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

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines
