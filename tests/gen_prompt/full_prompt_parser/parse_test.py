"""
test parsing for FullPromptParser
"""

from kaye.gen_prompt import FullPromptParserNode
from prompts import PROMPT1, PROMPT2, PROMPT3


class TestParse1:

    def test_root(self):
        tree = FullPromptParserNode.parse(PROMPT1)

        assert tree.depth == 0
        assert tree.parent is None
        assert len(tree.children) == 1
        assert tree.content == ""

    def test_project(self):
        tree = FullPromptParserNode.parse(PROMPT1)
        project = tree.children[0]

        assert project.name == "Project Title"
        assert project.depth == 1
        assert project.parent is tree
        assert len(project.children) == 3
        assert project.content == ""

    def test_sub1(self):
        tree = FullPromptParserNode.parse(PROMPT1)
        project = tree.children[0]
        sub = project.children[0]

        assert sub.name == "Description"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert (
            sub.content == """Brief overview of the project and its purpose."""
        )

    def test_sub2(self):
        tree = FullPromptParserNode.parse(PROMPT1)
        project = tree.children[0]
        sub = project.children[1]

        assert sub.name == "Installation"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == """Clone the repo and install dependencies."""

    def test_sub3(self):
        tree = FullPromptParserNode.parse(PROMPT1)
        project = tree.children[0]
        sub = project.children[2]

        assert sub.name == "License"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == """Licensed under the MIT License."""


class TestParse2:

    def test_root(self):
        tree = FullPromptParserNode.parse(PROMPT2)

        assert tree.depth == 0
        assert tree.parent is None
        assert len(tree.children) == 1
        assert tree.content == ""

    def test_project(self):
        tree = FullPromptParserNode.parse(PROMPT2)
        project = tree.children[0]

        assert project.depth == 1
        assert project.parent is tree
        assert len(project.children) == 5
        assert project.content == ""

    def test_description(self):
        tree = FullPromptParserNode.parse(PROMPT2)
        project = tree.children[0]
        sub = project.children[0]

        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert (
            sub.content
            == """A brief overview of the project, its purpose, and goals."""
        )

    def test_install(self):
        tree = FullPromptParserNode.parse(PROMPT2)
        project = tree.children[0]
        sub = project.children[1]

        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == """1. Clone the repo
2. Install dependencies
3. Run the application"""

    def test_usage1(self):
        tree = FullPromptParserNode.parse(PROMPT2)
        project = tree.children[0]
        sub = project["Usage"]

        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert (
            sub.content
            == """Provide instructions on how to use the application."""
        )

    def test_usage2(self):
        tree = FullPromptParserNode.parse(PROMPT2)
        project = tree.children[0]
        sub = project["Contributing"]

        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub.content == """1. Fork the repo
2. Create a new branch
3. Submit a pull request"""

    def test_license(self):
        tree = FullPromptParserNode.parse(PROMPT2)
        project = tree.children[0]
        sub = project["License"]

        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert (
            sub.content
            == """This project is licensed under the MIT License."""
        )


class TestParse3:

    def test_root(self):
        tree = FullPromptParserNode.parse(PROMPT3)

        assert tree.depth == 0
        assert tree.parent is None
        assert len(tree.children) == 1
        assert tree.content == ""

    def test_project(self):
        tree = FullPromptParserNode.parse(PROMPT3)
        project = tree["Main Title"]

        assert project.depth == 1
        assert project.parent is tree
        assert len(project.children) == 3
        assert project.content == ""

    def test_intro(self):
        tree = FullPromptParserNode.parse(PROMPT3)
        project = tree["Main Title"]
        node = project["Introduction"]

        assert node.depth == 2
        assert node.parent is project
        assert len(node.children) == 1
        assert node.content == """Brief introduction to the topic."""

    def test_intro_bg(self):
        tree = FullPromptParserNode.parse(PROMPT3)
        project = tree["Main Title"]
        parent = project["Introduction"]
        node = parent["Background"]

        assert node.depth == 3
        assert node.parent is parent
        assert len(node.children) == 1
        assert node.content == """Context or history relevant to the topic."""

    def test_intro_bg_mpt(self):
        tree = FullPromptParserNode.parse(PROMPT3)
        project = tree["Main Title"]
        parent = project["Introduction"]["Background"]
        node = parent["Importance"]

        assert node.depth == 4
        assert node.parent is parent
        assert len(node.children) == 1
        assert (
            node.content
            == """Why this topic matters in the current scenario."""
        )

    def test_intro_bg_mpt_obj(self):
        tree = FullPromptParserNode.parse(PROMPT3)
        project = tree["Main Title"]
        parent = project["Introduction"]["Background"]["Importance"]
        node = parent["Objective"]

        assert node.depth == 5
        assert node.parent is parent
        assert len(node.children) == 0
        assert node.content == """The primary goal of this document."""

    def test_met(self):
        tree = FullPromptParserNode.parse(PROMPT3)
        project = tree["Main Title"]
        node = project["Methods"]

        assert node.depth == 2
        assert node.parent is project
        assert len(node.children) == 1
        assert node.content == """Overview of the methodologies used."""

    def test_met_dc(self):
        tree = FullPromptParserNode.parse(PROMPT3)
        project = tree["Main Title"]
        parent = project["Methods"]
        node = parent["Data Collection"]

        assert node.depth == 3
        assert node.parent is parent
        assert len(node.children) == 1
        assert node.content == """How data was gathered for analysis."""

    def test_met_dc_tu(self):
        tree = FullPromptParserNode.parse(PROMPT3)
        project = tree["Main Title"]
        parent = project["Methods"]["Data Collection"]
        node = parent["Tools Used"]

        assert node.depth == 4
        assert node.parent is parent
        assert len(node.children) == 1
        assert node.content == """List of tools utilized during the project."""

    def test_met_dc_tu_fw(self):
        tree = FullPromptParserNode.parse(PROMPT3)
        project = tree["Main Title"]
        parent = project["Methods"]["Data Collection"]["Tools Used"]
        node = parent["Future Work"]

        assert node.depth == 5
        assert node.parent is parent
        assert len(node.children) == 0
        assert node.content == """Suggestions for future research or tasks."""

    def test_concl(self):
        tree = FullPromptParserNode.parse(PROMPT3)
        project = tree["Main Title"]
        node = project["Conclusion"]

        assert node.depth == 2
        assert node.parent is project
        assert len(node.children) == 0
        assert node.content == """Summarizing the findings and implications."""


class TestEmptyLine:  # source material contains various empty lines

    src = """
# Project Title




## Description
A brief overview of the project, its purpose, and goals.






## Installation
1. Clone the repo
2. Install dependencies
3. Run the application

## Usage

Provide instructions on how to use the application.













## Contributing
1. Fork the repo
2. Creat e anew branch
3. Submit a pull request





## License
This project is licensed under the MIT License.
"""

    def test_root(self):
        tree = FullPromptParserNode.parse(self.src)

        assert tree.depth == 0
        assert tree.parent is None
        assert len(tree.children) == 1
        assert tree.content == ""

    def test_project(self):
        tree = FullPromptParserNode.parse(self.src)
        project = tree.children[0]

        assert project.depth == 1
        assert project.parent is tree
        assert len(project) == 5
        assert project.content == ""

    def test_description(self):
        tree = FullPromptParserNode.parse(self.src)
        project = tree.children[0]
        sub = project["Description"]

        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert (
            sub.content
            == """A brief overview of the project, its purpose, and goals."""
        )

    def test_install(self):
        tree = FullPromptParserNode.parse(self.src)
        project = tree.children[0]
        sub = project["Installation"]

        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert sub.content == """1. Clone the repo
2. Install dependencies
3. Run the application"""

    def test_usage1(self):
        tree = FullPromptParserNode.parse(self.src)
        project = tree.children[0]
        sub = project["Usage"]

        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert (
            sub.content
            == """Provide instructions on how to use the application."""
        )

    def test_usage2(self):
        tree = FullPromptParserNode.parse(self.src)
        project = tree.children[0]
        sub = project["Contributing"]

        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert sub.content == """1. Fork the repo
2. Create a new branch
3. Submit a pull request"""

    def test_license(self):
        tree = FullPromptParserNode.parse(self.src)
        project = tree.children[0]
        sub = project["License"]

        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert (
            sub.content
            == """This project is licensed under the MIT License."""
        )


class TestEdge:  # various edge cases

    def test_empty1(_):  # total empty
        src = """"""

        tree = FullPromptParserNode.parse(src)
        assert tree.depth == 0
        assert tree.parent is None

        assert len(tree) == 0

    def test_empty2(_):
        src = "\n"

        tree = FullPromptParserNode.parse(src)
        assert tree.depth == 0
        assert tree.parent is None

        assert len(tree) == 0

    def test_empty3(_):
        src = "\n" * 10

        tree = FullPromptParserNode.parse(src)
        assert tree.depth == 0
        assert tree.parent is None

        assert len(tree) == 0
