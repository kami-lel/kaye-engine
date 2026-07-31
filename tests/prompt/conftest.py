import pytest


from copy import deepcopy
from unittest.mock import mock_open, patch


from kaye_engine.abbr_collection.abbr_data_loader import load_abbr_data
from kaye_engine.prompt.prompt_corpus_loader import load_corpus_tree
from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode

from kaye_engine.prompt import (
    TodayNode,
    AbbrNode,
    UsableAbbrNode,
    LanguageCodeNode,
    PLCNode,
)


@pytest.fixture(scope="session", autouse=True)
def _loaded_abbr_data():
    m = mock_open(read_data="{}")

    with patch("builtins.open", m):
        return load_abbr_data("dummy-abbrs-path.json")


@pytest.fixture(scope="session")
def corpus_testee1():
    root = PromptCorpusNode("○", None, [])
    proj = PromptCorpusNode("Project Title", root, [])

    PromptCorpusNode(
        "Description",
        proj,
        ["Brief overview of the project and its purpose."],
    )

    PromptCorpusNode(
        "Installation", proj, ["Clone the repo and install dependencies."]
    )

    PromptCorpusNode("License", proj, ["Licensed under the MIT License."])

    return root


@pytest.fixture(scope="session")
def corpus_testee2():
    root = PromptCorpusNode("○", None, [])
    proj = PromptCorpusNode("Project Title", root, [])

    PromptCorpusNode(
        "Description",
        proj,
        ["A brief overview of the project, its purpose, and goals."],
    )

    PromptCorpusNode(
        "Installation",
        proj,
        [
            "1. Clone the repo",
            "2. Install dependencies",
            "3. Run the application",
        ],
    )

    PromptCorpusNode(
        "Usage", proj, ["Provide instructions on how to use the application."]
    )

    contributing = PromptCorpusNode(
        "Contributing",
        proj,
        [
            "1. Fork the repo",
            "2. Create a new branch",
            "3. Submit a pull request",
        ],
    )

    PromptCorpusNode(
        "description",
        contributing,
        ["A step-by-step guide of how to contribute"],
    )

    PromptCorpusNode(
        "License", proj, ["This project is licensed under the MIT License."]
    )

    return root


@pytest.fixture(scope="session")
def corpus_testee3():
    root = PromptCorpusNode("○", None, [])
    proj = PromptCorpusNode("Main Title", root, [])

    intro = PromptCorpusNode(
        "Introduction", proj, ["Brief introduction to the topic."]
    )

    bg = PromptCorpusNode(
        "Background", intro, ["Context or history relevant to the topic."]
    )

    mpt = PromptCorpusNode(
        "Importance", bg, ["Why this topic matters in the current scenario."]
    )

    PromptCorpusNode("Objective", mpt, ["The primary goal of this document."])

    methods = PromptCorpusNode(
        "Methods", proj, ["Overview of the methodologies used."]
    )

    data = PromptCorpusNode(
        "Data Collection", methods, ["How data was gathered for analysis."]
    )

    tools = PromptCorpusNode(
        "Tools Used", data, ["List of tools utilized during the project."]
    )

    PromptCorpusNode(
        "Future Work", tools, ["Suggestions for future research or tasks."]
    )

    PromptCorpusNode(
        "Conclusion", proj, ["Summarizing the findings and implications."]
    )

    return root


@pytest.fixture(scope="session")
def corpus_dynamic_testee(corpus_testee3):
    tree = deepcopy(corpus_testee3)

    for node_type in (
        TodayNode,
        AbbrNode,
        UsableAbbrNode,
        LanguageCodeNode,
        PLCNode,
    ):
        node_type(tree)

    return tree


@pytest.fixture(scope="session")
def corpus():
    m = mock_open(read_data="""
# Project Title
## Description
Brief overview of the project and its purpose.

## Installation
Clone the repo and install dependencies.

## License
Licensed under the MIT License.
""")

    with patch("builtins.open", m):
        return load_corpus_tree(
            "prompt-conftest-default", "dummy-path.md", is_default_tree=True
        )
