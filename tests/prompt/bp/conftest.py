import pytest


from kaye_engine.prompt.blueprint.prompt_blueprint import PromptBlueprint
from tests.prompt.bp import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_1_PARTIAL_2_PRUNED,
    BLUEPRINT_1_EMPTY,
    BLUEPRINT_2_FULL,
    BLUEPRINT_2_PARTIAL_1,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_2,
    BLUEPRINT_3_EMPTY,
)


@pytest.fixture
def dynamic_bp_testee1(corpus_dynamic_testee):
    corpus = corpus_dynamic_testee
    text = """    ○
[x] ├── Main Title
[x] │   ├── Introduction
[x] │   │   └── Background
[x] │   │       └── Importance
[x] │   │           └── Objective
[x] │   ├── Methods
[x] │   │   └── Data Collection
[x] │   │       └── Tools Used
[x] │   │           └── Future Work
[x] │   └── Conclusion
[x] ├── (Today)
[x] ├── (Abbreviations)
[x] ├── (Usable Abbreviations)
[x] ├── (Languages Code)
[ ] └── (Programming Languages Code)"""

    return PromptBlueprint.parse(
        text, corpus_override=corpus, disable_prune=True
    )


@pytest.fixture
def dynamic_bp_testee_full(corpus_dynamic_testee):
    corpus = corpus_dynamic_testee

    text = """    ○
[x] ├── Main Title
[x] │   ├── Introduction
[x] │   │   └── Background
[x] │   │       └── Importance
[x] │   │           └── Objective
[x] │   ├── Methods
[x] │   │   └── Data Collection
[x] │   │       └── Tools Used
[x] │   │           └── Future Work
[x] │   └── Conclusion
[x] ├── (Today)
[x] ├── (Abbreviations)
[x] ├── (Usable Abbreviations)
[x] ├── (Languages Code)
[x] └── (Programming Languages Code)"""

    return PromptBlueprint.parse(
        text, corpus_override=corpus, disable_prune=True
    )


@pytest.fixture
def dynamic_bp_testee_empty(corpus_dynamic_testee):
    corpus = corpus_dynamic_testee

    text = """    ○
[ ] ├── Main Title
[ ] │   ├── Introduction
[ ] │   │   └── Background
[ ] │   │       └── Importance
[ ] │   │           └── Objective
[ ] │   ├── Methods
[ ] │   │   └── Data Collection
[ ] │   │       └── Tools Used
[ ] │   │           └── Future Work
[ ] │   └── Conclusion
[ ] ├── (Today)
[ ] ├── (Abbreviations)
[ ] ├── (Usable Abbreviations)
[ ] ├── (Languages Code)
[ ] └── (Programming Languages Code)"""

    return PromptBlueprint.parse(
        text, corpus_override=corpus, disable_prune=True
    )


@pytest.fixture(scope="session")
def dynamic_bp_testee2(corpus_dynamic_testee):
    bp_text = """ ○
[x] └── (Today)"""

    return PromptBlueprint.parse(
        bp_text, corpus_override=corpus_dynamic_testee, disable_prune=True
    )


@pytest.fixture(scope="session")
def dynamic_bp_testee3(corpus_dynamic_testee):
    bp_text = """ ○
[x] └── (Abbreviations)"""

    return PromptBlueprint.parse(
        bp_text, corpus_override=corpus_dynamic_testee, disable_prune=True
    )


@pytest.fixture(scope="session")
def dynamic_bp_testee4(corpus_dynamic_testee):
    bp_text = """ ○
[x] └── (Programming Languages Code)"""

    return PromptBlueprint.parse(
        bp_text, corpus_override=corpus_dynamic_testee, disable_prune=True
    )


@pytest.fixture(scope="session")
def dynamic_bp_testee5(corpus_dynamic_testee):
    bp_text = """ ○
[x] └── (Usable Abbreviations)"""

    return PromptBlueprint.parse(
        bp_text, corpus_override=corpus_dynamic_testee, disable_prune=True
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


# prompt 2 blueprints  ---------------------------------------------------------


@pytest.fixture(scope="class")
def bp_testee2full(corpus_testee2):
    corpus = corpus_testee2
    return PromptBlueprint.parse(
        BLUEPRINT_2_FULL, disable_prune=True, corpus_override=corpus
    )


@pytest.fixture(scope="class")
def bp_testee2pa1(corpus_testee2):
    corpus = corpus_testee2
    return PromptBlueprint.parse(
        BLUEPRINT_2_PARTIAL_1, disable_prune=True, corpus_override=corpus
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
