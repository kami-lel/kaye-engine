"""
test code for PromptParserNode
"""

from kaye.gen_prompt import PromptParserNode


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
        tree = PromptParserNode(self.src)

        assert tree.level == 0
        assert tree.parent is None
        assert tree.enable is True
        assert len(tree) == 1
        assert tree.content == ""

    def test_project(self):
        tree = PromptParserNode(self.src)
        project = tree["Project Title"]

        assert project.level == 1
        assert project.parent is tree
        assert project.enable is True
        assert len(project) == 3
        assert project.content == ""

    def test_sub1(self):
        tree = PromptParserNode(self.src)
        project = tree["Project Title"]
        sub = project["Description"]

        assert sub.level == 2
        assert sub.parent is project
        assert sub.enable is True
        assert len(sub) == 0
        assert (
            sub.content == """Brief overview of the project and its purpose."""
        )

    def test_sub2(self):
        tree = PromptParserNode(self.src)
        project = tree["Project Title"]
        sub = project["Installation"]

        assert sub.level == 2
        assert sub.parent is project
        assert sub.enable is True
        assert len(sub) == 0
        assert sub.content == """Clone the repo and install dependencies."""

    def test_sub3(self):
        tree = PromptParserNode(self.src)
        project = tree["Project Title"]
        sub = project["License"]

        assert sub.level == 2
        assert sub.parent is project
        assert sub.enable is True
        assert len(sub) == 0
        assert sub.content == """Licensed under the MIT License.
"""
