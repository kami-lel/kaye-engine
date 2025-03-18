"""
test function generate_heading_and_content_lines() for ``FullPromptParserNode``
"""

from kaye.gen_prompt import FullPromptParserNode
from prompts import PROMPT1, PROMPT2, PROMPT3, PROMPT_EMPTYLINES


class TestParse1:

    def test_project(self):
        tree = FullPromptParserNode.parse(PROMPT1)

        project = tree.children[0]

        opt = project.generate_heading_and_content_lines()
        print(opt)
        assert opt == ["# Project Title"]

    def test_sub1(self):
        tree = FullPromptParserNode.parse(PROMPT1)
        project = tree.children[0]
        sub = project.children[0]

        opt = sub.generate_heading_and_content_lines()
        print(opt)
        assert opt == [
            "## Description",
            "Brief overview of the project and its purpose.",
        ]

    def test_sub2(self):
        tree = FullPromptParserNode.parse(PROMPT1)
        project = tree.children[0]
        sub = project.children[1]

        opt = sub.generate_heading_and_content_lines()
        print(opt)
        assert opt == [
            "## Installation",
            "Clone the repo and install dependencies.",
        ]

    def test_sub3(self):
        tree = FullPromptParserNode.parse(PROMPT1)
        project = tree.children[0]
        sub = project.children[2]

        opt = sub.generate_heading_and_content_lines()
        print(opt)

        assert opt == ["## License", "Licensed under the MIT License."]
