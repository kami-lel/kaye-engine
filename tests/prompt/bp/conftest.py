import copy


import pytest


from kaye.gen_prompt.prompt_blueprint import PromptBlueprint


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
[x]     │   ├── {Programming Languages Code}
[x]     │   └── Data Collection
[x]     │       └── Tools Used
[x]     │           └── Future Work
[x]     │               └── {Today}
[x]     └── Conclusion"""

    return PromptBlueprint.parse(text, corpus_override=corpus)
