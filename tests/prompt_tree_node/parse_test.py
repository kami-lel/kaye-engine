"""
test parsing for PromptTreeNode
"""

from kaye import PromptTreeNode


class TestParse1:

    src = """
# Project Title

## Description
Brief overview of the project and its purpose.

## Installation
Clone the repo and install dependencies.


## License

Licensed under the MIT License.
"""

    def test_root(self):
        tree = PromptTreeNode(self.src)

        assert tree.level == 0
        assert tree.parent is None
        assert len(tree) == 1
        assert tree.content == ""

    def test_project(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]

        assert project.level == 1
        assert project.parent is tree
        assert len(project) == 3
        assert project.content == ""

    def test_sub1(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]
        sub = project["Description"]

        assert sub.level == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert (
            sub.content == """Brief overview of the project and its purpose."""
        )

    def test_sub2(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]
        sub = project["Installation"]

        assert sub.level == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert sub.content == """Clone the repo and install dependencies."""

    def test_sub3(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]
        sub = project["License"]

        assert sub.level == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert sub.content == """Licensed under the MIT License.
"""


class TestParse2:

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
2. Create a new branch
3. Submit a pull request

## License
This project is licensed under the MIT License.
"""

    def test_root(self):
        tree = PromptTreeNode(self.src)

        assert tree.level == 0
        assert tree.parent is None
        assert len(tree) == 1
        assert tree.content == ""

    def test_project(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]

        assert project.level == 1
        assert project.parent is tree
        assert len(project) == 5
        assert project.content == ""

    def test_description(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]
        sub = project["Description"]

        assert sub.level == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert (
            sub.content
            == """A brief overview of the project, its purpose, and goals."""
        )

    def test_install(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]
        sub = project["Installation"]

        assert sub.level == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert sub.content == """1. Clone the repo
2. Install dependencies
3. Run the application"""

    def test_usage1(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]
        sub = project["Usage"]

        assert sub.level == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert (
            sub.content
            == """Provide instructions on how to use the application."""
        )

    def test_usage2(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]
        sub = project["Contributing"]

        assert sub.level == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert sub.content == """1. Fork the repo
2. Create a new branch
3. Submit a pull request"""

    def test_license(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]
        sub = project["License"]

        assert sub.level == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert (
            sub.content == """This project is licensed under the MIT License.
"""
        )


class TestParse3:

    src = """
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
"""

    def test_root(self):
        tree = PromptTreeNode(self.src)

        assert tree.level == 0
        assert tree.parent is None
        assert len(tree) == 1
        assert tree.content == ""

    def test_project(self):
        tree = PromptTreeNode(self.src)
        project = tree["Main Title"]

        assert project.level == 1
        assert project.parent is tree
        assert len(project) == 3
        assert project.content == ""

    def test_intro(self):
        tree = PromptTreeNode(self.src)
        project = tree["Main Title"]
        node = project["Introduction"]

        assert node.level == 2
        assert node.parent is project
        assert len(node) == 1
        assert node.content == """Brief introduction to the topic."""

    def test_intro_bg(self):
        tree = PromptTreeNode(self.src)
        project = tree["Main Title"]
        parent = project["Introduction"]
        node = parent["Background"]

        assert node.level == 3
        assert node.parent is parent
        assert len(node) == 1
        assert node.content == """Context or history relevant to the topic."""

    def test_intro_bg_mpt(self):
        tree = PromptTreeNode(self.src)
        project = tree["Main Title"]
        parent = project["Introduction"]["Background"]
        node = parent["Importance"]

        assert node.level == 4
        assert node.parent is parent
        assert len(node) == 1
        assert (
            node.content
            == """Why this topic matters in the current scenario."""
        )

    def test_intro_bg_mpt_obj(self):
        tree = PromptTreeNode(self.src)
        project = tree["Main Title"]
        parent = project["Introduction"]["Background"]["Importance"]
        node = parent["Objective"]

        assert node.level == 5
        assert node.parent is parent
        assert len(node) == 0
        assert node.content == """The primary goal of this document."""

    def test_met(self):
        tree = PromptTreeNode(self.src)
        project = tree["Main Title"]
        node = project["Methods"]

        assert node.level == 2
        assert node.parent is project
        assert len(node) == 1
        assert node.content == """Overview of the methodologies used."""

    def test_met_dc(self):
        tree = PromptTreeNode(self.src)
        project = tree["Main Title"]
        parent = project["Methods"]
        node = parent["Data Collection"]

        assert node.level == 3
        assert node.parent is parent
        assert len(node) == 1
        assert node.content == """How data was gathered for analysis."""

    def test_met_dc_tu(self):
        tree = PromptTreeNode(self.src)
        project = tree["Main Title"]
        parent = project["Methods"]["Data Collection"]
        node = parent["Tools Used"]

        assert node.level == 4
        assert node.parent is parent
        assert len(node) == 1
        assert node.content == """List of tools utilized during the project."""

    def test_met_dc_tu_fw(self):
        tree = PromptTreeNode(self.src)
        project = tree["Main Title"]
        parent = project["Methods"]["Data Collection"]["Tools Used"]
        node = parent["Future Work"]

        assert node.level == 5
        assert node.parent is parent
        assert len(node) == 0
        assert node.content == """Suggestions for future research or tasks."""

    def test_concl(self):
        tree = PromptTreeNode(self.src)
        project = tree["Main Title"]
        node = project["Conclusion"]

        assert node.level == 2
        assert node.parent is project
        assert len(node) == 0
        assert node.content == """Summarizing the findings and implications.
"""


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
2. Create a new branch
3. Submit a pull request





## License
This project is licensed under the MIT License.
"""

    def test_root(self):
        tree = PromptTreeNode(self.src)

        assert tree.level == 0
        assert tree.parent is None
        assert len(tree) == 1
        assert tree.content == ""

    def test_project(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]

        assert project.level == 1
        assert project.parent is tree
        assert len(project) == 5
        assert project.content == ""

    def test_description(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]
        sub = project["Description"]

        assert sub.level == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert (
            sub.content
            == """A brief overview of the project, its purpose, and goals."""
        )

    def test_install(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]
        sub = project["Installation"]

        assert sub.level == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert sub.content == """1. Clone the repo
2. Install dependencies
3. Run the application"""

    def test_usage1(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]
        sub = project["Usage"]

        assert sub.level == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert (
            sub.content
            == """Provide instructions on how to use the application."""
        )

    def test_usage2(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]
        sub = project["Contributing"]

        assert sub.level == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert sub.content == """1. Fork the repo
2. Create a new branch
3. Submit a pull request"""

    def test_license(self):
        tree = PromptTreeNode(self.src)
        project = tree["Project Title"]
        sub = project["License"]

        assert sub.level == 2
        assert sub.parent is project
        assert len(sub) == 0
        assert (
            sub.content == """This project is licensed under the MIT License.
"""
        )


class TestEdge:  # various edge cases

    def test_empty1(_):  # total empty
        src = """"""

        tree = PromptTreeNode(src)
        assert tree.level == 0
        assert tree.parent is None

        assert len(tree) == 0

    def test_empty2(_):
        src = "\n"

        tree = PromptTreeNode(src)
        assert tree.level == 0
        assert tree.parent is None

        assert len(tree) == 0

    def test_empty3(_):
        src = "\n" * 10

        tree = PromptTreeNode(src)
        assert tree.level == 0
        assert tree.parent is None

        assert len(tree) == 0
