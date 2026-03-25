import pytest


from kaye.prompt.prompt_corpus_node import PromptCorpusNode
from kaye.prompt.prompt_corpus_loader import load_prompt_corpus_tree

from kaye.prompt import (
    TodayNode,
    AbbrNode,
    UsableAbbrNode,
    LanguageCodeNode,
    PLCNode,
)


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

    PromptCorpusNode(
        "Contributing",
        proj,
        [
            "1. Fork the repo",
            "2. Create a new branch",
            "3. Submit a pull request",
        ],
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


@pytest.fixture()
def corpus():
    return load_prompt_corpus_tree()
