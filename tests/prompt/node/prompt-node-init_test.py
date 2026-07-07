"""
prompt_node_init_test.py

Unit Tests (using pytest) for:

- PromptCorpusNode.__init__()
"""

import pytest


from kaye.prompt.prompt_corpus_node import PromptCorpusNode


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

    def test_structure(_):
        root = PromptCorpusNode("Main Title", None, [])
        intro = PromptCorpusNode(
            "Introduction", root, ["Brief introduction to the topic."]
        )
        bg = PromptCorpusNode(
            "Background", intro, ["Context or history relevant to the topic."]
        )
        mpt = PromptCorpusNode(
            "Importance",
            bg,
            ["Why this topic matters in the current scenario."],
        )
        objective = PromptCorpusNode(
            "Objective", mpt, ["The primary goal of this document."]
        )

        methods = PromptCorpusNode(
            "Methods", root, ["Overview of the methodologies used."]
        )
        data = PromptCorpusNode(
            "Data Collection", methods, ["How data was gathered for analysis."]
        )
        tools = PromptCorpusNode(
            "Tools Used", data, ["List of tools utilized during the project."]
        )
        works = PromptCorpusNode(
            "Future Work", tools, ["Suggestions for future research or tasks."]
        )
        conclusion = PromptCorpusNode(
            "Conclusion", root, ["Summarizing the findings and implications."]
        )

        print(root.generate_prompt_tree_preview(content_preview_lines=0))

        # perform tests --------------------------------------------------------
        # root
        len(root.children) == 3
        root.children[0] is intro
        root.children[1] is methods
        root.children[2] is conclusion

        # bg
        bg.parent is root
        len(bg.children) == 1
        bg.children[0] is mpt

        # mpt
        mpt.parent is bg
        len(mpt.children) == 1
        mpt.children[0] is objective

        # mpt
        mpt.parent is bg
        len(mpt.children) == 1
        mpt.children[0] is objective

        # objective
        objective.parent is mpt
        len(objective.children) == 0

        # methods
        methods.parent is root
        len(methods.children) == 1
        methods.children[0] is data

        # data
        data.parent is methods
        len(data.children) == 1
        data.children[0] is tools

        # tools
        tools.parent is methods
        len(tools.children) == 1
        tools.children[0] is works

        # works
        works.parent is methods
        len(works.children) == 1

        # conclusion
        conclusion.parent is root
        len(works.children) == 0


class TestAllowsDynamicNodeHeadingSyntax:  #####################################

    def test1(_):
        ipt = "(Abc Def)"
        opt = PromptCorpusNode(ipt, None, [])

        print(opt)
        assert opt.name == ipt

    def test2(_):
        ipt = "(Some Content ZZZ)"
        opt = PromptCorpusNode(ipt, None, [])

        print(opt)
        assert opt.name == ipt
