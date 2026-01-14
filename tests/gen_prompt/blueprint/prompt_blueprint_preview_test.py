"""
prompt_blueprint_preview_test.py

Unit Tests (using pytest) for: PromptBlueprint

- .generate_preview_tree()
- .__str__()
"""

import re


from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode
from tests.gen_prompt import PROMPT1, PROMPT2
from tests.gen_prompt.blueprint import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_1_EMPTY,
)

CORPUS1 = PromptCorpusNode.parse(PROMPT1)
CORPUS2 = PromptCorpusNode.parse(PROMPT2)


def _split_tree_and_comment(preview_tree):
    lines = preview_tree.splitlines()
    tree = "\n".join(lines[:-1])
    comment = lines[-1]
    return tree, comment


# test .generate_preview_tree()  ###############################################


# w/ all args
class TestAllArgs1:  # w/ corpus1
    # BUG BUG

    def test_full(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=3,
            preview_line_width=64,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, comment_content = _split_tree_and_comment(opt)

        assert tree_content == """    ○
[x] └── Project Title
[x]     ├── Description
        │   Brief overview of the project and its purpose.
[x]     ├── Installation
        │   Clone the repo and install dependencies.
[x]     └── License
            Licensed under the MIT License."""

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)

    def test_part1(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_PARTIAL_1

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=3,
            preview_line_width=64,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, _ = _split_tree_and_comment(opt)

        assert tree_content == """    ○
[ ] └── Project Title
[x]     ├── Description
        │   Brief overview of the project and its purpose.
[x]     ├── Installation
        │   Clone the repo and install dependencies.
[x]     └── License
            Licensed under the MIT License."""

    def test_part2(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_PARTIAL_2

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=3,
            preview_line_width=64,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, _ = _split_tree_and_comment(opt)

        assert tree_content == """    ○
[x] └── Project Title
[ ]     ├── Description
        │   Brief overview of the project and its purpose.
[x]     ├── Installation
        │   Clone the repo and install dependencies.
[x]     └── License
            Licensed under the MIT License."""

    def test_empty(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_EMPTY

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=3,
            preview_line_width=64,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, _ = _split_tree_and_comment(opt)

        assert tree_content == """    ○
[ ] └── Project Title
[ ]     ├── Description
        │   Brief overview of the project and its purpose.
[ ]     ├── Installation
        │   Clone the repo and install dependencies.
[ ]     └── License
            Licensed under the MIT License."""


# TODO use prompt 2;

# no content  ==================================================================

# no comment (nor content)  ====================================================

# full tree (nor content)  =====================================================

# default  =====================================================================

# test __str__()   #############################################################

# TODO TODO
