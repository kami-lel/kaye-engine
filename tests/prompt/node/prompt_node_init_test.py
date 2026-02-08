"""
prompt_node_init_test.py

Unit Tests (using pytest) for:

- PromptCorpusNode.__init__()
"""

import pytest


from kaye.gen_prompt.prompt_corpus_node import PromptCorpusNode


class TestInit:  ###############################################################

    def test1(_):
        heading = "Some Node"
        parent = None
        content_lines = []

        opt = PromptCorpusNode(heading, parent, content_lines)

        print(opt)
        assert opt.parent is None
        assert opt.name == heading
        assert len(opt.children) == 0
        assert opt._content_lines == content_lines

    def test2(_):
        heading = "Some Node"
        parent = None
        content_lines = ["aaa", "", "bbb"]

        opt = PromptCorpusNode(heading, parent, content_lines)

        print(opt)
        assert opt.parent is None
        assert opt.name == heading
        assert len(opt.children) == 0
        assert opt._content_lines == content_lines

    def test3(_):
        heading = "Some Node"
        parent = PromptCorpusNode("root", None, [])
        content_lines = ["aaa", "", "bbb"]

        opt = PromptCorpusNode(heading, parent, content_lines)

        print(opt)
        assert opt.parent is parent
        assert opt.name == heading
        assert len(opt.children) == 0
        assert opt._content_lines == content_lines

        assert parent.children[0] is opt

    # content lines trimming  --------------------------------------------------
    def test_trim1(_):
        content_lines = ["", "aaa", "", "zzz"]

        opt = PromptCorpusNode("AAA", None, content_lines)

        print(opt)

        assert opt._content_lines == ["aaa", "", "zzz"]

    def test_trim2(_):
        content_lines = ["", "", "", "aaa", "", "zzz"]

        opt = PromptCorpusNode("AAA", None, content_lines)

        print(opt)

        assert opt._content_lines == ["aaa", "", "zzz"]

    def test_trim3(_):
        content_lines = ["aaa", "", "zzz", "", ""]

        opt = PromptCorpusNode("AAA", None, content_lines)

        print(opt)

        assert opt._content_lines == ["aaa", "", "zzz"]

    def test_trim4(_):
        content_lines = ["", "aaa", "", "bbb", "", "ccc", "zzz", "", ""]

        opt = PromptCorpusNode("AAA", None, content_lines)

        print(opt)

        assert opt._content_lines == ["aaa", "", "bbb", "", "ccc", "zzz"]


class TestCheckName:  ##########################################################

    def test_fail1(_):
        ipt = "{Abc Def}"
        with pytest.raises(ValueError) as exec_info:
            PromptCorpusNode(ipt, None, [])

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "illegal heading syntax: '{Abc Def}'"

    def test_fail2(_):
        ipt = "{Some Content ZZZ}"
        with pytest.raises(ValueError) as exec_info:
            PromptCorpusNode(ipt, None, [])

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "illegal heading syntax: '{Some Content ZZZ}'"
