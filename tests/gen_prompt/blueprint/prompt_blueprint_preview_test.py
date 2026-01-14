"""
prompt_blueprint_preview_test.py

Unit Tests (using pytest) for: PromptBlueprint

- .generate_preview_tree()
- .__str__()
"""

import re


from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode
from tests.gen_prompt import PROMPT1, PROMPT2, PROMPT3
from tests.gen_prompt.blueprint import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_FULL_PREVIEW,
    BLUEPRINT_1_FULL_EMPTY,
    BLUEPRINT_1_FULL_PARTIAL_1,
    BLUEPRINT_1_FULL_PARTIAL_1_PREVIEW,
    BLUEPRINT_1_FULL_PARTIAL_2,
    BLUEPRINT_1_FULL_PARTIAL_2_PREVIEW,
    BLUEPRINT_2_FULL,
    BLUEPRINT_2_FULL_PREVIEW,
    BLUEPRINT_2_FULL_PARTIAL_1,
    BLUEPRINT_2_FULL_PARTIAL_1_PREVIEW,
    BLUEPRINT_2_FULL_EMPTY,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_FULL_PREVIEW,
    BLUEPRINT_3_FULL_PARTIAL_1,
    BLUEPRINT_3_FULL_PARTIAL_1_PREVIEW,
    BLUEPRINT_3_FULL_PARTIAL_2,
    BLUEPRINT_3_FULL_PARTIAL_2_PREVIEW,
    BLUEPRINT_3_FULL_EMPTY,
)

CORPUS1 = PromptCorpusNode.parse(PROMPT1)
CORPUS2 = PromptCorpusNode.parse(PROMPT2)
CORPUS3 = PromptCorpusNode.parse(PROMPT3)


def _split_tree_and_comment(preview_tree):
    lines = preview_tree.splitlines()
    tree = "\n".join(lines[:-1])
    comment = lines[-1]
    return tree, comment


# test .generate_preview_tree()  ###############################################


# w/ all args
class TestAllArgs1:  # w/ corpus1  *********************************************

    def test_full(self):
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

        assert tree_content == BLUEPRINT_1_FULL_PREVIEW

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)

    def test_part1(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_FULL_PARTIAL_1

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=3,
            preview_line_width=64,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, _ = _split_tree_and_comment(opt)

        assert tree_content == BLUEPRINT_1_FULL_PARTIAL_1_PREVIEW

    def test_part2(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_FULL_PARTIAL_2

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=3,
            preview_line_width=64,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, _ = _split_tree_and_comment(opt)

        assert tree_content == BLUEPRINT_1_FULL_PARTIAL_2_PREVIEW

    def test_empty(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_FULL_EMPTY

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


class TestAllArgs2:  # w/ corpus2  *********************************************

    def test_full(self):
        corpus = CORPUS2
        bp_text = BLUEPRINT_2_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=3,
            preview_line_width=64,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, comment_content = _split_tree_and_comment(opt)

        assert tree_content == BLUEPRINT_2_FULL_PREVIEW

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)

    def test_part1(_):
        corpus = CORPUS2
        bp_text = BLUEPRINT_2_FULL_PARTIAL_1

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=3,
            preview_line_width=64,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, _ = _split_tree_and_comment(opt)

        assert tree_content == BLUEPRINT_2_FULL_PARTIAL_1_PREVIEW

    def test_empty(_):
        corpus = CORPUS2
        bp_text = BLUEPRINT_2_FULL_EMPTY

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
        │   A brief overview of the project, its purpose, and goals.
[ ]     ├── Installation
        │   1. Clone the repo
        │   2. Install dependencies
        │   3. Run the application
[ ]     ├── Usage
        │   Provide instructions on how to use the application.
[ ]     ├── Contributing
        │   1. Fork the repo
        │   2. Create a new branch
        │   3. Submit a pull request
[ ]     └── License
            This project is licensed under the MIT License."""


class TestAllArgs3:  # w/ corpus1  *********************************************

    def test_full(self):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=3,
            preview_line_width=64,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, comment_content = _split_tree_and_comment(opt)

        assert tree_content == BLUEPRINT_3_FULL_PREVIEW
        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)

    def test_part1(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_FULL_PARTIAL_1

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=3,
            preview_line_width=64,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, _ = _split_tree_and_comment(opt)

        assert tree_content == BLUEPRINT_3_FULL_PARTIAL_1_PREVIEW

    def test_part2(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_FULL_PARTIAL_2

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=3,
            preview_line_width=64,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, _ = _split_tree_and_comment(opt)

        assert tree_content == BLUEPRINT_3_FULL_PARTIAL_2_PREVIEW

    def test_empty(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_FULL_EMPTY

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
[ ] └── Main Title
[ ]     ├── Introduction
        │   Brief introduction to the topic.
[ ]     │   └── Background
        │       Context or history relevant to the topic.
[ ]     │       └── Importance
        │           Why this topic matters in the current scenario.
[ ]     │           └── Objective
        │               The primary goal of this document.
[ ]     ├── Methods
        │   Overview of the methodologies used.
[ ]     │   └── Data Collection
        │       How data was gathered for analysis.
[ ]     │       └── Tools Used
        │           List of tools utilized during the project.
[ ]     │           └── Future Work
        │               Suggestions for future research or tasks.
[ ]     └── Conclusion
            Summarizing the findings and implications."""


# no content  ==================================================================


# w/ all args
class TestNoContent1:  # w/ corpus1  *******************************************

    def test_full(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=0,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, comment_content = _split_tree_and_comment(opt)

        assert tree_content == """    ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     └── License"""

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)

    def test_part1(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_FULL_PARTIAL_1

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=0,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, _ = _split_tree_and_comment(opt)

        assert tree_content == """    ○
[ ] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     └── License"""

    def test_part2(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_FULL_PARTIAL_2

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=0,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, _ = _split_tree_and_comment(opt)

        assert tree_content == """    ○
[x] └── Project Title
[ ]     ├── Description
[x]     ├── Installation
[x]     └── License"""

    def test_empty(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_FULL_EMPTY

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=0,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, _ = _split_tree_and_comment(opt)

        assert tree_content == """    ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     └── License"""


class TestNoContent3:  # w/ corpus1  *******************************************

    def test_full(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=0,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, comment_content = _split_tree_and_comment(opt)

        assert tree_content == """    ○
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

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)

    def test_part1(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_FULL_PARTIAL_1

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=0,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, _ = _split_tree_and_comment(opt)

        assert tree_content == """    ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[ ]     │           └── Future Work
[x]     └── Conclusion"""

    def test_part2(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_FULL_PARTIAL_2

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=0,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, _ = _split_tree_and_comment(opt)

        assert tree_content == """    ○
[x] └── Main Title
[ ]     ├── Introduction
[x]     │   └── Background
[ ]     │       └── Importance
[x]     │           └── Objective
[ ]     ├── Methods
[x]     │   └── Data Collection
[ ]     │       └── Tools Used
[x]     │           └── Future Work
[ ]     └── Conclusion"""

    def test_empty(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_FULL_EMPTY

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=0,
            show_full_tree=False,
            hide_comment=False,
        )

        print(opt)
        tree_content, _ = _split_tree_and_comment(opt)

        assert tree_content == """    ○
[ ] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[ ]     │           └── Future Work
[ ]     └── Conclusion"""


# no comment (nor content)  ====================================================


# w/ all args
class TestNoComment:  # w/ corpus1  *******************************************

    def test1(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=0,
            show_full_tree=False,
            hide_comment=True,
        )

        print(opt)
        assert opt == """    ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     └── License"""

    def test3(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree(
            preview_line_count=0,
            show_full_tree=False,
            hide_comment=True,
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


# pruned tree  =================================================================

# TODO

# full tree (nor content)  =====================================================

# TODO

# default  =====================================================================


class TestDft:

    def test1(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree()

        print(opt)
        tree_content, comment_content = _split_tree_and_comment(opt)

        assert tree_content == BLUEPRINT_1_FULL_PREVIEW

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)

    def test2(_):
        corpus = CORPUS2
        bp_text = BLUEPRINT_2_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree()

        print(opt)
        tree_content, comment_content = _split_tree_and_comment(opt)

        assert tree_content == BLUEPRINT_2_FULL_PREVIEW

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)

    def test3(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = bp.generate_preview_tree()

        print(opt)
        tree_content, comment_content = _split_tree_and_comment(opt)

        assert tree_content == BLUEPRINT_3_FULL_PREVIEW

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)


# test __str__()   #############################################################


class TestStr:

    def test1(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = str(bp)

        print(opt)
        tree_content, comment_content = _split_tree_and_comment(opt)

        assert tree_content == BLUEPRINT_1_FULL_PREVIEW

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)

    def test2(_):
        corpus = CORPUS2
        bp_text = BLUEPRINT_2_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = str(bp)

        print(opt)
        tree_content, comment_content = _split_tree_and_comment(opt)

        assert tree_content == BLUEPRINT_2_FULL_PREVIEW

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)

    def test3(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)
        opt = str(bp)

        print(opt)
        tree_content, comment_content = _split_tree_and_comment(opt)

        assert tree_content == BLUEPRINT_3_FULL_PREVIEW

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)
