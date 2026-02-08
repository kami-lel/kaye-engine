import pytest


from kaye.gen_prompt.prompt_corpus_node import PromptCorpusNode


@pytest.fixture()
def test_prompt_corpus_tree1():
    root = PromptCorpusNode("Project Title", None, [])

    PromptCorpusNode(
        "Description", root, ["Brief overview of the project and its purpose."]
    )

    PromptCorpusNode(
        "Installation", root, ["Clone the repo and install dependencies."]
    )

    PromptCorpusNode("License", root, ["Licensed under the MIT Li]cense."])

    return root


@pytest.fixture()
def test_prompt_corpus_tree2():
    root = PromptCorpusNode("Project Title", None, [])

    PromptCorpusNode(
        "Description", root, ["Brief overview of the project and its purpose."]
    )

    PromptCorpusNode(
        "Installation",
        root,
        [
            "1. Clone the repo",
            "2. Install dependencies",
            "3. Run the application",
        ],
    )

    PromptCorpusNode(
        "Usage", root, ["Provide instructions on how to use the application."]
    )

    PromptCorpusNode(
        "Contributing",
        root,
        [
            "1. Fork the repo",
            "2. Create a new branch",
            "3. Submit a pull request",
        ],
    )

    PromptCorpusNode("License", root, ["Licensed under the MIT Li]cense."])

    return root


@pytest.fixture()
def test_prompt_corpus_tree3():
    root = PromptCorpusNode("Main Title", None, [])

    intro = PromptCorpusNode(
        "Introduction", root, ["Brief introduction to the topic."]
    )

    bg = PromptCorpusNode(
        "Background", intro, ["Context or history relevant to the topic."]
    )

    mpt = PromptCorpusNode(
        "Importance", bg, ["Why this topic matters in the current scenario."]
    )

    PromptCorpusNode("Objective", mpt, ["The primary goal of this document."])

    methods = PromptCorpusNode(
        "Methods", root, ["Overview of the methodologies used."]
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
        "Conclusion", root, ["Summarizing the findings and implications."]
    )

    return root
