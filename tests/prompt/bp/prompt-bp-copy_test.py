"""
prompt-bp-copy_test.py

Unit Tests (using pytest) for: PromptCorpusNode.__copy__()
"""

from copy import copy


class TestParse1:  #############################################################

    def test_root(_, test_corpus1):
        src_node = test_corpus1

        opt = copy(src_node)
        print(str(opt))

        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_project(_, test_corpus1):
        tree = test_corpus1
        src_node = tree.children[0]

        opt = copy(src_node)

        print(str(opt))
        assert src_node.name == opt.name
        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_sub1(_, test_corpus1):
        tree = test_corpus1
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
    def test_root(_, test_corpus2):
        src_node = test_corpus2

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_project(_, test_corpus2):
        tree = test_corpus2
        src_node = tree.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_description(_, test_corpus2):
        tree = test_corpus2
        project = tree.children[0]
        src_node = project.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_install(_, test_corpus2):
        tree = test_corpus2
        project = tree.children[0]
        src_node = project.children[1]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_usage1(_, test_corpus2):
        tree = test_corpus2
        project = tree.children[0]
        src_node = project.children[2]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines


class TestParse3:  #############################################################

    def test_root(_, test_corpus3):
        src_node = test_corpus3

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_project(_, test_corpus3):
        tree = test_corpus3
        src_node = tree.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_intro(_, test_corpus3):
        tree = test_corpus3
        project = tree.children[0]
        src_node = project.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_intro_bg(_, test_corpus3):
        tree = test_corpus3
        project = tree.children[0]
        parent = project.children[0]
        src_node = parent.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_intro_bg_mpt(_, test_corpus3):
        tree = test_corpus3
        project = tree.children[0]
        parent = project.children[0].children[0]
        src_node = parent.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines

    def test_intro_bg_mpt_obj(_, test_corpus3):
        tree = test_corpus3
        project = tree.children[0]
        parent = project.children[0].children[0].children[0]
        src_node = parent.children[0]

        opt = copy(src_node)
        print(str(opt))

        assert src_node.depth == opt.depth
        assert src_node.parent is opt.parent
        assert len(opt.children) == 0
        assert src_node._content_lines == opt._content_lines
