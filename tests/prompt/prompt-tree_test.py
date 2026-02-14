"""
prompt_tree_test.py

Unit Tests (using pytest) for: load_prompt_corpus_tree
"""

import pytest

from kaye.prompt.prompt_corpus_loader import load_prompt_corpus_tree


# test using PROMPT1  ##########################################################
@pytest.fixture()
def prompt_tree1():
    return load_prompt_corpus_tree(prompt_corpus_text_override="""
# Project Title
## Description
Brief overview of the project and its purpose.

## Installation
Clone the repo and install dependencies.

## License
Licensed under the MIT License.
""")


class TestParse1:

    def test_root(self, prompt_tree1):

        assert prompt_tree1.depth == 0
        assert prompt_tree1.parent is None
        assert len(prompt_tree1.children) == 1
        assert prompt_tree1._content_lines == []

    def test_project(self, prompt_tree1):
        project = prompt_tree1.children[0]

        print(
            prompt_tree1.generate_prompt_tree_preview(content_preview_lines=0)
        )

        assert project.name == "Project Title"
        assert project.depth == 1
        assert project.parent is prompt_tree1
        assert len(project.children) == 3
        assert project._content_lines == []

    def test_sub1(self, prompt_tree1):
        project = prompt_tree1.children[0]
        sub = project.children[0]

        assert sub.name == "Description"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "Brief overview of the project and its purpose."
        ]

    def test_sub2(self, prompt_tree1):
        project = prompt_tree1.children[0]
        sub = project.children[1]

        assert sub.name == "Installation"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "Clone the repo and install dependencies."
        ]

    def test_sub3(self, prompt_tree1):
        project = prompt_tree1.children[0]
        sub = project.children[2]

        assert sub.name == "License"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == ["Licensed under the MIT License."]


# test using PROMPT2  ##########################################################
@pytest.fixture()
def prompt_tree2():
    return load_prompt_corpus_tree(prompt_corpus_text_override="""
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


class TestParse2:

    def test_root(self, prompt_tree2):

        assert prompt_tree2.depth == 0
        assert prompt_tree2.parent is None
        assert len(prompt_tree2.children) == 1
        assert prompt_tree2._content_lines == []

    def test_project(self, prompt_tree2):
        project = prompt_tree2.children[0]

        assert project.name == "Project Title"
        assert project.depth == 1
        assert project.parent is prompt_tree2
        assert len(project.children) == 5
        assert project._content_lines == []

    def test_description(self, prompt_tree2):
        project = prompt_tree2.children[0]
        sub = project.children[0]

        assert sub.name == "Description"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "A brief overview of the project, its purpose, and goals."
        ]

    def test_install(self, prompt_tree2):
        project = prompt_tree2.children[0]
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

    def test_usage1(self, prompt_tree2):
        project = prompt_tree2.children[0]
        sub = project.children[2]

        assert sub.name == "Usage"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "Provide instructions on how to use the application."
        ]

    def test_usage2(self, prompt_tree2):
        project = prompt_tree2.children[0]
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

    def test_license(self, prompt_tree2):
        project = prompt_tree2.children[0]
        sub = project.children[4]

        assert sub.name == "License"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "This project is licensed under the MIT License."
        ]


# test using PROMPT3  ##########################################################
@pytest.fixture()
def prompt_tree3():
    return load_prompt_corpus_tree(prompt_corpus_text_override="""
# Main Title

## Introduction
Brief introduction to the topic.

### Background
Context or history relevant to the topic.

#### Importance
Why this topic matters in the current scenario.

##### Objective
The primary goal of this document.

## Methods
Overview of the methodologies used.

### Data Collection
How data was gathered for analysis.

#### Tools Used
List of tools utilized during the project.

##### Future Work
Suggestions for future research or tasks.

## Conclusion
Summarizing the findings and implications.
""")


class TestParse3:

    def test_root(self, prompt_tree3):
        assert prompt_tree3.depth == 0
        assert prompt_tree3.parent is None
        assert len(prompt_tree3.children) == 1
        assert prompt_tree3._content_lines == []

    def test_project(self, prompt_tree3):
        project = prompt_tree3.children[0]

        assert project.name == "Main Title"
        assert project.depth == 1
        assert project.parent is prompt_tree3
        assert len(project.children) == 3
        assert project._content_lines == []

    def test_intro(self, prompt_tree3):
        project = prompt_tree3.children[0]
        node = project.children[0]

        print(repr(prompt_tree3))

        assert node.name == "Introduction"
        assert node.depth == 2
        assert node.parent is project
        assert len(node.children) == 1
        assert node._content_lines == ["Brief introduction to the topic."]

    def test_intro_bg(self, prompt_tree3):
        project = prompt_tree3.children[0]
        parent = project.children[0]
        node = parent.children[0]

        print(repr(prompt_tree3))
        assert node.name == "Background"
        assert node.depth == 3
        assert node.parent is parent
        assert len(node.children) == 1
        assert node._content_lines == [
            "Context or history relevant to the topic."
        ]

    def test_intro_bg_mpt(self, prompt_tree3):
        project = prompt_tree3.children[0]
        parent = project.children[0].children[0]
        node = parent.children[0]

        print(repr(prompt_tree3))
        assert node.name == "Importance"
        assert node.depth == 4
        assert node.parent is parent
        assert len(node.children) == 1
        assert node._content_lines == [
            "Why this topic matters in the current scenario."
        ]

    def test_intro_bg_mpt_obj(self, prompt_tree3):
        project = prompt_tree3.children[0]
        parent = project.children[0].children[0].children[0]
        node = parent.children[0]

        print(repr(prompt_tree3))
        assert node.name == "Objective"
        assert node.depth == 5
        assert node.parent is parent
        assert len(node.children) == 0
        assert node._content_lines == ["The primary goal of this document."]

    def test_met(self, prompt_tree3):
        project = prompt_tree3.children[0]
        node = project.children[1]

        print(repr(prompt_tree3))
        assert node.name == "Methods"
        assert node.depth == 2
        assert node.parent is project
        assert len(node.children) == 1
        assert node._content_lines == ["Overview of the methodologies used."]

    def test_met_dc(self, prompt_tree3):
        project = prompt_tree3.children[0]
        parent = project.children[1]
        node = parent.children[0]

        print(repr(prompt_tree3))
        assert node.name == "Data Collection"
        assert node.depth == 3
        assert node.parent is parent
        assert len(node.children) == 1
        assert node._content_lines == ["How data was gathered for analysis."]

    def test_met_dc_tu(self, prompt_tree3):
        project = prompt_tree3.children[0]
        parent = project.children[1].children[0]
        node = parent.children[0]

        print(repr(prompt_tree3))
        assert node.name == "Tools Used"
        assert node.depth == 4
        assert node.parent is parent
        assert len(node.children) == 1
        assert node._content_lines == [
            "List of tools utilized during the project."
        ]

    def test_met_dc_tu_fw(self, prompt_tree3):
        project = prompt_tree3.children[0]
        parent = project.children[1].children[0].children[0]
        node = parent.children[0]

        assert node.name == "Future Work"
        assert node.depth == 5
        assert node.parent is parent
        assert len(node.children) == 0
        assert node._content_lines == [
            "Suggestions for future research or tasks."
        ]

    def test_concl(self, prompt_tree3):
        project = prompt_tree3.children[0]
        node = project.children[2]

        assert node.name == "Conclusion"
        assert node.depth == 2
        assert node.parent is project
        assert len(node.children) == 0
        assert node._content_lines == [
            "Summarizing the findings and implications."
        ]


# empty lines tests  ###########################################################
@pytest.fixture()
def prompt_tree_empty():
    return load_prompt_corpus_tree(prompt_corpus_text_override="""

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


class TestEmptyLine:  # source material contains various empty lines

    def test_root(self, prompt_tree_empty):
        assert prompt_tree_empty.depth == 0
        assert prompt_tree_empty.parent is None
        assert len(prompt_tree_empty.children) == 1
        assert prompt_tree_empty._content_lines == []

    def test_project(self, prompt_tree_empty):
        project = prompt_tree_empty.children[0]

        assert project.name == "Project Title"
        assert project.depth == 1
        assert project.parent is prompt_tree_empty
        assert len(project.children) == 5
        assert project._content_lines == []

    def test_description(self, prompt_tree_empty):
        project = prompt_tree_empty.children[0]
        sub = project.children[0]

        assert sub.name == "Description"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "A brief overview of the project, its purpose, and goals.",
        ]

    def test_install(self, prompt_tree_empty):
        project = prompt_tree_empty.children[0]
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

    def test_usage1(self, prompt_tree_empty):
        project = prompt_tree_empty.children[0]
        sub = project.children[2]

        assert sub.name == "Usage"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "Provide instructions on how to use the application.",
        ]

    def test_usage2(self, prompt_tree_empty):
        project = prompt_tree_empty.children[0]
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

    def test_license(self, prompt_tree_empty):
        project = prompt_tree_empty.children[0]
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

        tree = load_prompt_corpus_tree(prompt_corpus_text_override=src)
        assert tree.depth == 0
        assert tree.parent is None

        assert len(tree.children) == 0

    def test_empty2(_):
        src = "\n"

        tree = load_prompt_corpus_tree(prompt_corpus_text_override=src)
        assert tree.depth == 0
        assert tree.parent is None

        assert len(tree.children) == 0

    def test_empty3(_):
        src = "\n" * 10

        tree = load_prompt_corpus_tree(prompt_corpus_text_override=src)
        assert tree.depth == 0
        assert tree.parent is None

        assert len(tree.children) == 0


class TestForbiddenHeading:  ###################################################

    def test1(_):
        with pytest.raises(ValueError) as exec_info:
            load_prompt_corpus_tree(prompt_corpus_text_override="""# Title
## {Some}""")

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "illegal heading syntax: '{Some}'"


class TestSingleton:  ##########################################################

    def test1(_):
        attempt1 = load_prompt_corpus_tree()
        attempt2 = load_prompt_corpus_tree()
        attempt3 = load_prompt_corpus_tree()

        assert attempt1 is attempt2
        assert attempt2 is attempt3
