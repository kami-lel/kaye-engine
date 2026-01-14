"""
prompt_blueprint_full_test.py

Unit Tests (using pytest) for: PromptBlueprint

- .create_full_blueprint()
- .create_empty_blueprint()
"""

from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode

from tests.gen_prompt.node.testees import PROMPT1, PROMPT2

# test .create_full_blueprint()  ###############################################


# TODO TODO TODO
def test1():  # test using PROMPT1
    blueprint = PromptBlueprint.create_full_blueprint(
        PromptCorpusNode.parse(PROMPT1)
    )

    opt = blueprint.generate_preview_tree(
        preview_line_count=0, hide_comment=True
    )

    print(opt)
    assert opt == """    ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     ├── Usage
[x]     ├── Contributing
[x]     └── License"""


def test2():  # test using PROMPT2
    blueprint = PromptBlueprint.create_full_blueprint(
        PromptCorpusNode.parse(PROMPT2)
    )

    opt = blueprint.generate_preview_tree(
        preview_line_count=0, hide_comment=True
    )

    print(opt)
    assert opt == """    ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[x]     ├── Methods
[x]     │   └── Data Collection
[x]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""


# test .create_empty_blueprint()  ##############################################
