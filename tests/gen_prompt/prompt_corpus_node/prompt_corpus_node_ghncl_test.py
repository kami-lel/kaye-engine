"""
test public function ``.generate_heading_and_content_lines()`` for ``class PromptCorpusNode``
"""

from kaye.gen_prompt import PromptCorpusNode
from tests.gen_prompt.prompt_corpus_node.testees import (
    PROMPT1,
    PROMPT2,
    PROMPT3,
)

# BUG


class TestParse1:  # tes use PROMPT1

    def test_project(self):
        tree = PromptCorpusNode.parse(PROMPT1)

        project = tree.children[0]

        opt = project.generate_heading_and_content_lines()
        print(opt)
        assert opt == ["# Project Title"]

    def test_sub1(self):
        tree = PromptCorpusNode.parse(PROMPT1)
        project = tree.children[0]
        sub = project.children[0]

        opt = sub.generate_heading_and_content_lines()
        print(opt)
        assert opt == [
            "## Description",
            "Brief overview of the project and its purpose.",
        ]

    def test_sub2(self):
        tree = PromptCorpusNode.parse(PROMPT1)
        project = tree.children[0]
        sub = project.children[1]

        opt = sub.generate_heading_and_content_lines()
        print(opt)
        assert opt == [
            "## Installation",
            "Clone the repo and install dependencies.",
        ]

    def test_sub3(self):
        tree = PromptCorpusNode.parse(PROMPT1)
        project = tree.children[0]
        sub = project.children[2]

        opt = sub.generate_heading_and_content_lines()
        print(opt)

        assert opt == ["## License", "Licensed under the MIT License."]


class TestParse2:  # test use PROMPT2

    def test_project(self):
        tree = PromptCorpusNode.parse(PROMPT2)
        project = tree.children[0]

        opt = project.generate_heading_and_content_lines()
        print(opt)
        assert opt == ["# Project Title"]

    def test_description(self):
        tree = PromptCorpusNode.parse(PROMPT2)
        project = tree.children[0]
        sub = project.children[0]

        opt = sub.generate_heading_and_content_lines()
        print(opt)
        assert opt == [
            "## Description",
            "A brief overview of the project, its purpose, and goals.",
        ]

    def test_usage1(self):
        tree = PromptCorpusNode.parse(PROMPT2)
        project = tree.children[0]
        sub = project.children[2]

        opt = sub.generate_heading_and_content_lines()
        print(opt)
        assert opt == [
            "## Usage",
            "Provide instructions on how to use the application.",
        ]

    def test_contribute(self):
        tree = PromptCorpusNode.parse(PROMPT2)
        project = tree.children[0]
        sub = project.children[3]

        opt = sub.generate_heading_and_content_lines()
        print(opt)
        assert opt == [
            "## Contributing",
            "1. Fork the repo",
            "2. Create a new branch",
            "3. Submit a pull request",
        ]


class TestParse3:  # test use PROMPT3

    def test_project(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]

        opt = project.generate_heading_and_content_lines()
        print(opt)
        assert opt == ["# Main Title"]

    def test_intro(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        node = project.children[0]

        opt = node.generate_heading_and_content_lines()
        print(opt)

        assert opt == [
            "## Introduction",
            "Brief introduction to the topic.",
        ]

    def test_intro_bg(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[0]
        node = parent.children[0]

        opt = node.generate_heading_and_content_lines()
        print(opt)

        assert opt == [
            "### Background",
            "Context or history relevant to the topic.",
        ]

    def test_intro_bg_mpt(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[0].children[0]
        node = parent.children[0]

        opt = node.generate_heading_and_content_lines()
        print(opt)
        assert opt == [
            "#### Importance",
            "Why this topic matters in the current scenario.",
        ]

    def test_intro_bg_mpt_obj(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[0].children[0].children[0]
        node = parent.children[0]

        opt = node.generate_heading_and_content_lines()
        print(opt)
        assert opt == ["##### Objective", "The primary goal of this document."]

    def test_met(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        node = project.children[1]

        opt = node.generate_heading_and_content_lines()
        print(opt)

        assert opt == ["## Methods", "Overview of the methodologies used."]

    def test_met_dc(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[1]
        node = parent.children[0]

        opt = node.generate_heading_and_content_lines()
        print(opt)

        assert opt == [
            "### Data Collection",
            "How data was gathered for analysis.",
        ]

    def test_met_dc_tu(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[1].children[0]
        node = parent.children[0]

        opt = node.generate_heading_and_content_lines()
        print(opt)

        assert opt == [
            "#### Tools Used",
            "List of tools utilized during the project.",
        ]

    def test_met_dc_tu_fw(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[1].children[0].children[0]
        node = parent.children[0]

        opt = node.generate_heading_and_content_lines()
        print(opt)

        assert opt == [
            "##### Future Work",
            "Suggestions for future research or tasks.",
        ]

    def test_concl(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        node = project.children[2]

        opt = node.generate_heading_and_content_lines()
        print(opt)

        assert opt == [
            "## Conclusion",
            "Summarizing the findings and implications.",
        ]
