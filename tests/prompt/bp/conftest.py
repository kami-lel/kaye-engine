import copy


import pytest


from kaye.prompt.prompt_blueprint import PromptBlueprint
from tests.prompt.bp import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_1_PARTIAL_2_PRUNED,
    BLUEPRINT_1_EMPTY,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_2,
    BLUEPRINT_3_EMPTY,
)


@pytest.fixture
def dynamic_bp_testee1(corpus_testee3):
    corpus = copy.deepcopy(corpus_testee3)
    text = """    ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   ├── {Usable Abbreviations}
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


# prompt 1 blueprints  ---------------------------------------------------------


@pytest.fixture(scope="class")
def bp_testee1full(corpus_testee1):
    corpus = corpus_testee1
    return PromptBlueprint.parse(
        BLUEPRINT_1_FULL, disable_prune=True, corpus_override=corpus
    )


@pytest.fixture(scope="class")
def bp_testee1pa1(corpus_testee1):
    corpus = corpus_testee1
    return PromptBlueprint.parse(
        BLUEPRINT_1_PARTIAL_1, disable_prune=True, corpus_override=corpus
    )


@pytest.fixture(scope="class")
def bp_testee1pa2(corpus_testee1):
    corpus = corpus_testee1
    return PromptBlueprint.parse(
        BLUEPRINT_1_PARTIAL_2, disable_prune=True, corpus_override=corpus
    )


@pytest.fixture(scope="class")
def bp_testee1pa2pruned(corpus_testee1):
    corpus = corpus_testee1
    return PromptBlueprint.parse(
        BLUEPRINT_1_PARTIAL_2_PRUNED,
        disable_prune=True,
        corpus_override=corpus,
    )


@pytest.fixture(scope="class")
def bp_testee1empty(corpus_testee1):
    corpus = corpus_testee1
    return PromptBlueprint.parse(
        BLUEPRINT_1_EMPTY, disable_prune=True, corpus_override=corpus
    )


# prompt 3 blueprints  ---------------------------------------------------------


@pytest.fixture(scope="class")
def bp_testee3full(corpus_testee3):
    corpus = corpus_testee3
    return PromptBlueprint.parse(
        BLUEPRINT_3_FULL, disable_prune=True, corpus_override=corpus
    )


@pytest.fixture(scope="class")
def bp_testee3pa1(corpus_testee3):
    corpus = corpus_testee3
    return PromptBlueprint.parse(
        BLUEPRINT_3_PARTIAL_1, disable_prune=True, corpus_override=corpus
    )


@pytest.fixture(scope="class")
def bp_testee3pa2(corpus_testee3):
    corpus = corpus_testee3
    return PromptBlueprint.parse(
        BLUEPRINT_3_PARTIAL_2, disable_prune=True, corpus_override=corpus
    )


@pytest.fixture(scope="class")
def bp_testee3empty(corpus_testee3):
    corpus = corpus_testee3
    return PromptBlueprint.parse(
        BLUEPRINT_3_EMPTY, disable_prune=True, corpus_override=corpus
    )
