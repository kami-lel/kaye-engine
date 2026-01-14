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
    BLUEPRINT_1_FULL_PARTIAL_1,
    BLUEPRINT_1_FULL_PARTIAL_2,
    BLUEPRINT_1_FULL_EMPTY,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_FULL_PARTIAL_1,
    BLUEPRINT_3_FULL_PARTIAL_2,
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


class TestAllArgs3:  # w/ corpus1  *********************************************

    def test_full(_):
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

        assert tree_content == """    ○
[x] └── Main Title
[x]     ├── Introduction
        │   Brief introduction to the topic.
[x]     │   └── Background
        │       Context or history relevant to the topic.
[x]     │       └── Importance
        │           Why this topic matters in the current scenario.
[x]     │           └── Objective
        │               The primary goal of this document.
[x]     ├── Methods
        │   Overview of the methodologies used.
[x]     │   └── Data Collection
        │       How data was gathered for analysis.
[x]     │       └── Tools Used
        │           List of tools utilized during the project.
[x]     │           └── Future Work
        │               Suggestions for future research or tasks.
[x]     └── Conclusion
            Summarizing the findings and implications."""

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

        assert tree_content == """    ○
[x] └── Main Title
[x]     ├── Introduction
        │   Brief introduction to the topic.
[x]     │   └── Background
        │       Context or history relevant to the topic.
[x]     │       └── Importance
        │           Why this topic matters in the current scenario.
[x]     │           └── Objective
        │               The primary goal of this document.
[ ]     ├── Methods
        │   Overview of the methodologies used.
[ ]     │   └── Data Collection
        │       How data was gathered for analysis.
[ ]     │       └── Tools Used
        │           List of tools utilized during the project.
[ ]     │           └── Future Work
        │               Suggestions for future research or tasks.
[x]     └── Conclusion
            Summarizing the findings and implications."""

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

        assert tree_content == """    ○
[x] └── Main Title
[ ]     ├── Introduction
        │   Brief introduction to the topic.
[x]     │   └── Background
        │       Context or history relevant to the topic.
[ ]     │       └── Importance
        │           Why this topic matters in the current scenario.
[x]     │           └── Objective
        │               The primary goal of this document.
[ ]     ├── Methods
        │   Overview of the methodologies used.
[x]     │   └── Data Collection
        │       How data was gathered for analysis.
[ ]     │       └── Tools Used
        │           List of tools utilized during the project.
[x]     │           └── Future Work
        │               Suggestions for future research or tasks.
[ ]     └── Conclusion
            Summarizing the findings and implications."""

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


# TODO use prompt3 (multi lines content)

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
# TODO TODO

# full tree (nor content)  =====================================================

# default  =====================================================================

# test __str__()   #############################################################
