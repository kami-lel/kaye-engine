"""
prompt-tree-empty_test.py

Unit Tests (using pytest) for:

load_corpus_tree
"""

from unittest.mock import mock_open, patch

import pytest

from kaye_engine.prompt.prompt_corpus_loader import load_corpus_tree

# pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def prompt_tree_fenced():
    m = mock_open(
        read_data="""
# Project

## Snippet
Before the fence.

```
line1


line2
```

After the fence.

## Prose
Some text.




More text.
"""
    )

    with patch("builtins.open", m):
        return load_corpus_tree("prompt-tree-fenced-test", "dummy-path.md")


@pytest.fixture(scope="session")
def prompt_tree_empty():
    m = mock_open(read_data="""

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

    with patch("builtins.open", m):
        return load_corpus_tree("prompt-tree-empty-test", "dummy-path.md")


# pytest #######################################################################


class TestEmptyLine:  # source material contains various empty lines

    def test_root(self, prompt_tree_empty):
        assert prompt_tree_empty.depth == 0
        assert prompt_tree_empty.parent is None
        assert prompt_tree_empty._content_lines == ["", ""]

    def test_project(self, prompt_tree_empty):
        project = prompt_tree_empty.children[0]

        assert project.name == "Project Title"
        assert project.depth == 1
        assert project.parent is prompt_tree_empty
        assert len(project.children) == 5
        assert project._content_lines == [""]

    def test_description(self, prompt_tree_empty):
        project = prompt_tree_empty.children[0]
        sub = project.children[0]

        assert sub.name == "Description"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "A brief overview of the project, its purpose, and goals.",
            "",
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
            "",
        ]

    def test_usage1(self, prompt_tree_empty):
        project = prompt_tree_empty.children[0]
        sub = project.children[2]

        assert sub.name == "Usage"
        assert sub.depth == 2
        assert sub.parent is project
        assert len(sub.children) == 0
        assert sub._content_lines == [
            "",
            "Provide instructions on how to use the application.",
            "",
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
            "",
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
            "",
        ]


class TestEmptyLineFencedCodeBlock:
    # blank lines inside a fenced code block must survive verbatim,
    # while a blank-line run outside the fence still collapses to one

    def test_snippet_preserves_fenced_blank_lines(self, prompt_tree_fenced):
        project = prompt_tree_fenced.children[0]
        snippet = project.children[0]

        assert snippet.name == "Snippet"
        assert snippet._content_lines == [
            "Before the fence.",
            "",
            "```",
            "line1",
            "",
            "",
            "line2",
            "```",
            "",
            "After the fence.",
            "",
        ]

    def test_prose_still_collapses_unfenced_blank_runs(self, prompt_tree_fenced):
        project = prompt_tree_fenced.children[0]
        prose = project.children[1]

        assert prose.name == "Prose"
        assert prose._content_lines == [
            "Some text.",
            "",
            "More text.",
            "",
        ]
