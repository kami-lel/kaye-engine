"""
test .parse() and instance creation for ``class PromptCorpusNode``
"""

from kaye.gen_prompt import PromptCorpusNode
from tests.gen_prompt.prompt_corpus_node.testees import (
    PROMPT1,
    PROMPT2,
    PROMPT3,
    PROMPT_EMPTY_LINES,
)


class TestParse1:  # test using PROMPT1

    def test_root(self):
        tree = PromptCorpusNode.parse(PROMPT1)

        assert tree.depth == 0
        assert tree.parent is None
        assert len(tree.children) == 1
        assert tree.content == []

    def test_project(self):
        tree = PromptCorpusNode.parse(PROMPT1)
        project = tree.children[0]

        assert project.name == "Project Title"
        assert project.depth == 1
        assert project.parent is tree
        assert len(project.children) == 3
        assert project.content == []

    def test_sub1(self):
        tree = PromptCorpusNode.parse(PROMPT1)
        project = tree.children[0]
        sub = project.children[0]

        assert sub.name == "Description"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == [
            "Brief overview of the project and its purpose.",
            "",
        ]

    def test_sub2(self):
        tree = PromptCorpusNode.parse(PROMPT1)
        project = tree.children[0]
        sub = project.children[1]

        assert sub.name == "Installation"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == ["Clone the repo and install dependencies.", ""]

    def test_sub3(self):
        tree = PromptCorpusNode.parse(PROMPT1)
        project = tree.children[0]
        sub = project.children[2]

        assert sub.name == "License"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == ["Licensed under the MIT License.", ""]


class TestParse2:  # test using PROMPT2
    def test_root(self):
        tree = PromptCorpusNode.parse(PROMPT2)

        assert tree.depth == 0
        assert tree.parent is None
        assert len(tree.children) == 1
        assert tree.content == []

    def test_project(self):
        tree = PromptCorpusNode.parse(PROMPT2)
        project = tree.children[0]

        assert project.name == "Project Title"
        assert project.depth == 1
        assert project.parent is tree
        assert len(project.children) == 5
        assert project.content == []

    def test_description(self):
        tree = PromptCorpusNode.parse(PROMPT2)
        project = tree.children[0]
        sub = project.children[0]

        assert sub.name == "Description"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == [
            "A brief overview of the project, its purpose, and goals.",
            "",
        ]

    def test_install(self):
        tree = PromptCorpusNode.parse(PROMPT2)
        project = tree.children[0]
        sub = project.children[1]
        assert sub.name == "Installation"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == [
            "1. Clone the repo",
            "2. Install dependencies",
            "3. Run the application",
            "",
        ]

    def test_usage1(self):
        tree = PromptCorpusNode.parse(PROMPT2)
        project = tree.children[0]
        sub = project.children[2]

        assert sub.name == "Usage"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == [
            "Provide instructions on how to use the application.",
            "",
        ]

    def test_usage2(self):
        tree = PromptCorpusNode.parse(PROMPT2)
        project = tree.children[0]
        sub = project.children[3]

        assert sub.name == "Contributing"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == [
            "1. Fork the repo",
            "2. Create a new branch",
            "3. Submit a pull request",
            "",
        ]

    def test_license(self):
        tree = PromptCorpusNode.parse(PROMPT2)
        project = tree.children[0]
        sub = project.children[4]

        assert sub.name == "License"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == [
            "This project is licensed under the MIT License.",
            "",
        ]


class TestParse3:  # test using PROMPT3

    def test_root(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        assert tree.depth == 0
        assert tree.parent is None
        assert len(tree.children) == 1
        assert tree.content == []

    def test_project(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]

        assert project.name == "Main Title"
        assert project.depth == 1
        assert project.parent is tree
        assert len(project.children) == 3
        assert project.content == []

    def test_intro(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        node = project.children[0]

        assert node.name == "Introduction"
        assert node.depth == 2
        assert node.parent is project
        assert len(node.children) == 1
        assert node.content == ["Brief introduction to the topic.", ""]

    def test_intro_bg(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[0]
        node = parent.children[0]

        assert node.name == "Background"
        assert node.depth == 3
        assert node.parent is parent
        assert len(node.children) == 1
        assert node.content == [
            "Context or history relevant to the topic.",
            "",
        ]

    def test_intro_bg_mpt(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[0].children[0]
        node = parent.children[0]

        assert node.name == "Importance"
        assert node.depth == 4
        assert node.parent is parent
        assert len(node.children) == 1
        assert node.content == [
            "Why this topic matters in the current scenario.",
            "",
        ]

    def test_intro_bg_mpt_obj(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[0].children[0].children[0]
        node = parent.children[0]

        assert node.name == "Objective"
        assert node.depth == 5
        assert node.parent is parent
        assert len(node.children) == 0
        assert node.content == ["The primary goal of this document.", ""]

    def test_met(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        node = project.children[1]

        assert node.name == "Methods"
        assert node.depth == 2
        assert node.parent is project
        assert len(node.children) == 1
        assert node.content == ["Overview of the methodologies used.", ""]

    def test_met_dc(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[1]
        node = parent.children[0]

        assert node.name == "Data Collection"
        assert node.depth == 3
        assert node.parent is parent
        assert len(node.children) == 1
        assert node.content == ["How data was gathered for analysis.", ""]

    def test_met_dc_tu(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[1].children[0]
        node = parent.children[0]

        assert node.name == "Tools Used"
        assert node.depth == 4
        assert node.parent is parent
        assert len(node.children) == 1
        assert node.content == [
            "List of tools utilized during the project.",
            "",
        ]

    def test_met_dc_tu_fw(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[1].children[0].children[0]
        node = parent.children[0]

        assert node.name == "Future Work"
        assert node.depth == 5
        assert node.parent is parent
        assert len(node.children) == 0
        assert node.content == [
            "Suggestions for future research or tasks.",
            "",
        ]

    def test_concl(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        node = project.children[2]

        assert node.name == "Conclusion"
        assert node.depth == 2
        assert node.parent is project
        assert len(node.children) == 0
        assert node.content == [
            "Summarizing the findings and implications.",
            "",
        ]


class TestEmptyLine:  # source material contains various empty lines

    def test_root(self):
        tree = PromptCorpusNode.parse(PROMPT_EMPTY_LINES)

        assert tree.depth == 0
        assert tree.parent is None
        assert len(tree.children) == 1
        assert tree.content == []

    def test_project(self):
        tree = PromptCorpusNode.parse(PROMPT_EMPTY_LINES)
        project = tree.children[0]

        assert project.name == "Project Title"
        assert project.depth == 1
        assert project.parent is tree
        assert len(project.children) == 5
        assert project.content == []

    def test_description(self):
        tree = PromptCorpusNode.parse(PROMPT_EMPTY_LINES)
        project = tree.children[0]
        sub = project.children[0]

        assert sub.name == "Description"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == [
            "A brief overview of the project, its purpose, and goals.",
            "",
        ]

    def test_install(self):
        tree = PromptCorpusNode.parse(PROMPT_EMPTY_LINES)
        project = tree.children[0]
        sub = project.children[1]

        assert sub.name == "Installation"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == [
            "1. Clone the repo",
            "2. Install dependencies",
            "3. Run the application",
            "",
        ]

    def test_usage1(self):
        tree = PromptCorpusNode.parse(PROMPT_EMPTY_LINES)
        project = tree.children[0]
        sub = project.children[2]

        assert sub.name == "Usage"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == [
            "",
            "Provide instructions on how to use the application.",
            "",
        ]

    def test_usage2(self):
        tree = PromptCorpusNode.parse(PROMPT_EMPTY_LINES)
        project = tree.children[0]
        sub = project.children[3]

        assert sub.name == "Contributing"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == [
            "1. Fork the repo",
            "2. Create a new branch",
            "3. Submit a pull request",
            "",
        ]

    def test_license(self):
        tree = PromptCorpusNode.parse(PROMPT_EMPTY_LINES)
        project = tree.children[0]
        sub = project.children[4]

        assert sub.name == "License"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == [
            "This project is licensed under the MIT License.",
            "",
        ]


class TestEdge:  # various edge cases

    def test_empty1(_):  # total empty
        src = """"""

        tree = PromptCorpusNode.parse(src)
        assert tree.depth == 0
        assert tree.parent is None

        assert len(tree.children) == 0

    def test_empty2(_):
        src = "\n"

        tree = PromptCorpusNode.parse(src)
        assert tree.depth == 0
        assert tree.parent is None

        assert len(tree.children) == 0

    def test_empty3(_):
        src = "\n" * 10

        tree = PromptCorpusNode.parse(src)
        assert tree.depth == 0
        assert tree.parent is None

        assert len(tree.children) == 0
