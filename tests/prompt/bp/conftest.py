import copy


import pytest


from kaye.prompt.prompt_blueprint import PromptBlueprint


@pytest.fixture(scope="session")
def dynamic_bp_testee1(corpus_testee3):
    corpus = copy.deepcopy(corpus_testee3)
    text = """    ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           ├── Objective
[x]     │           └── {Abbreviations}
[x]     ├── Methods
[ ]     │   ├── {Programming Languages Code}
[x]     │   └── Data Collection
[x]     │       └── Tools Used
[x]     │           └── Future Work
[x]     │               └── {Today}
[x]     └── Conclusion"""

    return PromptBlueprint.parse(
        text, corpus_override=corpus, disable_prune=True
    )


@pytest.fixture(scope="session")
def dynamic_bp_testee2(corpus_testee1):
    bp_text = """ ○
[x] └── {Today}"""

    return PromptBlueprint.parse(
        bp_text, corpus_override=corpus_testee1, disable_prune=True
    )


@pytest.fixture(scope="session")
def dynamic_bp_testee3(corpus_testee1):
    bp_text = """ ○
[x] └── {Abbreviations}"""

    return PromptBlueprint.parse(
        bp_text, corpus_override=corpus_testee1, disable_prune=True
    )


@pytest.fixture(scope="session")
def dynamic_bp_testee4(corpus_testee1):
    bp_text = """ ○
[x] └── {Programming Languages Code}"""

    return PromptBlueprint.parse(
        bp_text, corpus_override=corpus_testee1, disable_prune=True
    )


@pytest.fixture(scope="session")
def dynamic_bp_testee5(corpus_testee1):
    bp_text = """ ○
[x] └── {Usable Abbreviations}"""

    return PromptBlueprint.parse(
        bp_text, corpus_override=corpus_testee1, disable_prune=True
    )
