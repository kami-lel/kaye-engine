"""
test .parse() and instance creation for ``class PromptCorpusNode``
"""

from kaye.gen_prompt import PromptCorpusNode
from tests.prompt import (
    PROMPT1,
    PROMPT2,
    PROMPT3,
)


# test using PROMPT1  ##########################################################
class TestParse1:

    tree = PromptCorpusNode.parse(PROMPT1)

    def test_root(self):

        assert self.tree.depth == 0
        assert self.tree.parent is None
        assert len(self.tree.children) == 1
        assert self.tree._content_lines == []

    def test_project(self):
        project = self.tree.children[0]

        assert project.name == "Project Title"
        assert project.depth == 1
        assert project.parent is self.tree
        assert len(project.children) == 3
        assert project._content_lines == []

    def test_sub1(self):
        project = self.tree.children[0]
        sub = project.children[0]

        assert sub.name == "Description"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "Brief overview of the project and its purpose."
        ]

    def test_sub2(self):
        project = self.tree.children[0]
        sub = project.children[1]

        assert sub.name == "Installation"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "Clone the repo and install dependencies."
        ]

    def test_sub3(self):
        project = self.tree.children[0]
        sub = project.children[2]

        assert sub.name == "License"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == ["Licensed under the MIT License."]


# test using PROMPT2  ##########################################################
class TestParse2:

    tree = PromptCorpusNode.parse(PROMPT2)

    def test_root(self):

        assert self.tree.depth == 0
        assert self.tree.parent is None
        assert len(self.tree.children) == 1
        assert self.tree._content_lines == []

    def test_project(self):
        project = self.tree.children[0]

        assert project.name == "Project Title"
        assert project.depth == 1
        assert project.parent is self.tree
        assert len(project.children) == 5
        assert project._content_lines == []

    def test_description(self):
        project = self.tree.children[0]
        sub = project.children[0]

        assert sub.name == "Description"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "A brief overview of the project, its purpose, and goals."
        ]

    def test_install(self):
        project = self.tree.children[0]
        sub = project.children[1]
        assert sub.name == "Installation"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "1. Clone the repo",
            "2. Install dependencies",
            "3. Run the application",
        ]

    def test_usage1(self):
        project = self.tree.children[0]
        sub = project.children[2]

        assert sub.name == "Usage"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "Provide instructions on how to use the application."
        ]

    def test_usage2(self):
        project = self.tree.children[0]
        sub = project.children[3]

        assert sub.name == "Contributing"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "1. Fork the repo",
            "2. Create a new branch",
            "3. Submit a pull request",
        ]

    def test_license(self):
        project = self.tree.children[0]
        sub = project.children[4]

        assert sub.name == "License"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "This project is licensed under the MIT License."
        ]


# test using PROMPT3  ##########################################################
class TestParse3:

    tree = PromptCorpusNode.parse(PROMPT3)
    # BUGs

    def test_root(self):
        assert self.tree.depth == 0
        assert self.tree.parent is None
        assert len(self.tree.children) == 1
        assert self.tree._content_lines == []

    def test_project(self):
        project = self.tree.children[0]

        assert project.name == "Main Title"
        assert project.depth == 1
        assert project.parent is self.tree
        assert len(project.children) == 3
        assert project._content_lines == []

    def test_intro(self):
        project = self.tree.children[0]
        node = project.children[0]

        print(repr(self.tree))

        assert node.name == "Introduction"
        assert node.depth == 2
        assert node.parent is project
        assert len(node.children) == 1
        assert node._content_lines == ["Brief introduction to the topic."]

    def test_intro_bg(self):
        project = self.tree.children[0]
        parent = project.children[0]
        node = parent.children[0]

        print(repr(self.tree))
        assert node.name == "Background"
        assert node.depth == 3
        assert node.parent is parent
        assert len(node.children) == 1
        assert node._content_lines == [
            "Context or history relevant to the topic."
        ]

    def test_intro_bg_mpt(self):
        project = self.tree.children[0]
        parent = project.children[0].children[0]
        node = parent.children[0]

        print(repr(self.tree))
        assert node.name == "Importance"
        assert node.depth == 4
        assert node.parent is parent
        assert len(node.children) == 1
        assert node._content_lines == [
            "Why this topic matters in the current scenario."
        ]

    def test_intro_bg_mpt_obj(self):
        project = self.tree.children[0]
        parent = project.children[0].children[0].children[0]
        node = parent.children[0]

        print(repr(self.tree))
        assert node.name == "Objective"
        assert node.depth == 5
        assert node.parent is parent
        assert len(node.children) == 0
        assert node._content_lines == ["The primary goal of this document."]

    def test_met(self):
        project = self.tree.children[0]
        node = project.children[1]

        print(repr(self.tree))
        assert node.name == "Methods"
        assert node.depth == 2
        assert node.parent is project
        assert len(node.children) == 1
        assert node._content_lines == ["Overview of the methodologies used."]

    def test_met_dc(self):
        project = self.tree.children[0]
        parent = project.children[1]
        node = parent.children[0]

        print(repr(self.tree))
        assert node.name == "Data Collection"
        assert node.depth == 3
        assert node.parent is parent
        assert len(node.children) == 1
        assert node._content_lines == ["How data was gathered for analysis."]

    def test_met_dc_tu(self):
        project = self.tree.children[0]
        parent = project.children[1].children[0]
        node = parent.children[0]

        print(repr(self.tree))
        assert node.name == "Tools Used"
        assert node.depth == 4
        assert node.parent is parent
        assert len(node.children) == 1
        assert node._content_lines == [
            "List of tools utilized during the project."
        ]

    def test_met_dc_tu_fw(self):
        project = self.tree.children[0]
        parent = project.children[1].children[0].children[0]
        node = parent.children[0]

        assert node.name == "Future Work"
        assert node.depth == 5
        assert node.parent is parent
        assert len(node.children) == 0
        assert node._content_lines == [
            "Suggestions for future research or tasks."
        ]

    def test_concl(self):
        project = self.tree.children[0]
        node = project.children[2]

        assert node.name == "Conclusion"
        assert node.depth == 2
        assert node.parent is project
        assert len(node.children) == 0
        assert node._content_lines == [
            "Summarizing the findings and implications."
        ]


# empty lines tests  ###########################################################
class TestEmptyLine:  # source material contains various empty lines

    tree = PromptCorpusNode.parse("""
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
2. Create a new branch
3. Submit a pull request





## License
This project is licensed under the MIT License.
""")

    def test_root(self):
        assert self.tree.depth == 0
        assert self.tree.parent is None
        assert len(self.tree.children) == 1
        assert self.tree._content_lines == []

    def test_project(self):
        project = self.tree.children[0]

        assert project.name == "Project Title"
        assert project.depth == 1
        assert project.parent is self.tree
        assert len(project.children) == 5
        assert project._content_lines == []

    def test_description(self):
        project = self.tree.children[0]
        sub = project.children[0]

        assert sub.name == "Description"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "A brief overview of the project, its purpose, and goals.",
        ]

    def test_install(self):
        project = self.tree.children[0]
        sub = project.children[1]

        assert sub.name == "Installation"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "1. Clone the repo",
            "2. Install dependencies",
            "3. Run the application",
        ]

    def test_usage1(self):
        project = self.tree.children[0]
        sub = project.children[2]

        assert sub.name == "Usage"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "Provide instructions on how to use the application.",
        ]

    def test_usage2(self):
        project = self.tree.children[0]
        sub = project.children[3]

        assert sub.name == "Contributing"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "1. Fork the repo",
            "2. Create a new branch",
            "3. Submit a pull request",
        ]

    def test_license(self):
        project = self.tree.children[0]
        sub = project.children[4]

        assert sub.name == "License"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "This project is licensed under the MIT License.",
        ]


# edge cases  ##################################################################
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


class TestForbiddenHeading:  ###################################################

    def test1(_):
        pass  # TODO
