"""
prompt-node-parse_test.py

Unit Tests (using pytest) for:

- PromptCorpusNode.parse()
"""

from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode


class TestParseIgnoresHeadingsInsideFence:  ####################################

    def test_heading_shaped_line_inside_fence_is_not_a_child(_):
        text_lines = [
            "Intro text.",
            "",
            "```md",
            "# not a heading",
            "content of the fenced example",
            "```",
            "",
            "More text.",
        ]

        opt = PromptCorpusNode.parse("Root", None, text_lines)

        print(opt)
        assert len(opt.children) == 0
        assert opt._content_lines == text_lines

    def test_real_heading_outside_fence_still_splits(_):
        text_lines = [
            "Intro text.",
            "```md",
            "fenced content",
            "```",
            "# Real Heading",
            "child content",
        ]

        opt = PromptCorpusNode.parse("Root", None, text_lines)

        print(opt)
        assert len(opt.children) == 1
        assert opt.children[0].name == "Real Heading"
        assert opt.children[0]._content_lines == ["child content"]
        assert opt._content_lines == [
            "Intro text.",
            "```md",
            "fenced content",
            "```",
        ]

    def test_heading_lookalike_inside_bare_fence(_):
        text_lines = [
            "```",
            "## also not a heading",
            "```",
        ]

        root = PromptCorpusNode("Root", None, [])
        opt = PromptCorpusNode.parse("Section", root, text_lines)

        print(opt)
        assert len(opt.children) == 0
        assert opt._content_lines == text_lines


class TestParseIgnoresHeadingsInsideTagBlock:  ################################

    def test_heading_shaped_line_inside_tag_block_is_not_a_child(_):
        text_lines = [
            "Intro text.",
            "<some-tag>",
            "# not a heading",
            "",
            "content of the example",
            "</some-tag>",
        ]

        opt = PromptCorpusNode.parse("Root", None, text_lines)

        print(opt)
        assert len(opt.children) == 0
        assert opt._content_lines == text_lines

    def test_real_heading_after_tag_block_still_splits(_):
        text_lines = [
            "<t>",
            "# inside",
            "</t>",
            "# Real Heading",
            "child content",
        ]

        opt = PromptCorpusNode.parse("Root", None, text_lines)

        print(opt)
        assert [c.name for c in opt.children] == ["Real Heading"]
        assert opt._content_lines == text_lines[:3]
