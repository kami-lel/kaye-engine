"""
prompt-bp-gen_test.py

Unit Tests (using pytest) for: PromptBlueprint

- .generate_blueprint()
"""

import re


from kaye_engine.prompt.blueprint.prompt_blueprint import PromptBlueprint

from tests.prompt.bp import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_FULL_PREVIEW,
    BLUEPRINT_1_EMPTY,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_1_PREVIEW,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_1_PARTIAL_2_PREVIEW,
    BLUEPRINT_2_FULL,
    BLUEPRINT_2_PREVIEW,
    BLUEPRINT_2_PARTIAL_1,
    BLUEPRINT_2_PARTIAL_1_PREVIEW,
    BLUEPRINT_2_PARTIAL_1_PRUNED,
    BLUEPRINT_2_EMPTY,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_FULL_PREVIEW,
    BLUEPRINT_3_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_1_PREVIEW,
    BLUEPRINT_3_PARTIAL_1_PRUNED,
    BLUEPRINT_3_PARTIAL_2,
    BLUEPRINT_3_PARTIAL_2_PREVIEW,
    BLUEPRINT_3_PARTIAL_2_PRUNED,
    BLUEPRINT_3_EMPTY,
    _split_content_and_comment,
)


# w/ all args  #################################################################
class TestAllArgs1:  # =========================================================

    def test_full(_, corpus_testee1):
        corpus = corpus_testee1
        bp_text = BLUEPRINT_1_FULL

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=3,
            content_preview_width=64,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, comment_content = _split_content_and_comment(opt)

        assert tree_content == BLUEPRINT_1_FULL_PREVIEW

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)

    def test_part1(_, corpus_testee1):
        corpus = corpus_testee1
        bp_text = BLUEPRINT_1_PARTIAL_1

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=3,
            content_preview_width=64,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, _ = _split_content_and_comment(opt)

        assert tree_content == BLUEPRINT_1_PARTIAL_1_PREVIEW

    def test_part2(_, corpus_testee1):
        corpus = corpus_testee1
        bp_text = BLUEPRINT_1_PARTIAL_2

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=3,
            content_preview_width=64,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, _ = _split_content_and_comment(opt)

        assert tree_content == BLUEPRINT_1_PARTIAL_2_PREVIEW

    def test_empty(_, corpus_testee1):
        corpus = corpus_testee1
        bp_text = BLUEPRINT_1_EMPTY

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=3,
            content_preview_width=64,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, _ = _split_content_and_comment(opt)

        assert tree_content == """    ○
[ ] └── Project Title
[ ]     ├── Description
        │   Brief overview of the project and its purpose.
[ ]     ├── Installation
        │   Clone the repo and install dependencies.
[ ]     └── License
            Licensed under the MIT License."""


class TestAllArgs2:  # =========================================================

    def test_full(_, corpus_testee2):
        corpus = corpus_testee2
        bp_text = BLUEPRINT_2_FULL

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=3,
            content_preview_width=64,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, comment_content = _split_content_and_comment(opt)

        assert tree_content == BLUEPRINT_2_PREVIEW

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)

    def test_part1(_, corpus_testee2):
        corpus = corpus_testee2
        bp_text = BLUEPRINT_2_PARTIAL_1

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=3,
            content_preview_width=64,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, _ = _split_content_and_comment(opt)

        assert tree_content == BLUEPRINT_2_PARTIAL_1_PREVIEW

    def test_empty(_, corpus_testee2):
        corpus = corpus_testee2
        bp_text = BLUEPRINT_2_EMPTY

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=3,
            content_preview_width=64,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, _ = _split_content_and_comment(opt)

        assert tree_content == """    ○
[ ] └── Project Title
[ ]     ├── Description
        │   A brief overview of the project, its purpose, and go
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
[ ]     │   └── description
        │       A step-by-step guide of how to contribute
[ ]     └── License
            This project is licensed under the MIT License."""


class TestAllArgs3:  # =========================================================

    def test_full(_, corpus_testee3):
        corpus = corpus_testee3
        bp_text = BLUEPRINT_3_FULL

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=3,
            content_preview_width=64,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, comment_content = _split_content_and_comment(opt)

        assert tree_content == BLUEPRINT_3_FULL_PREVIEW
        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)

    def test_part1(_, corpus_testee3):
        corpus = corpus_testee3
        bp_text = BLUEPRINT_3_PARTIAL_1

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=3,
            content_preview_width=64,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, _ = _split_content_and_comment(opt)

        assert tree_content == BLUEPRINT_3_PARTIAL_1_PREVIEW

    def test_part2(_, corpus_testee3):
        corpus = corpus_testee3
        bp_text = BLUEPRINT_3_PARTIAL_2

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=3,
            content_preview_width=64,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, _ = _split_content_and_comment(opt)

        assert tree_content == BLUEPRINT_3_PARTIAL_2_PREVIEW

    def test_empty(_, corpus_testee3):
        corpus = corpus_testee3
        bp_text = BLUEPRINT_3_EMPTY

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=3,
            content_preview_width=64,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, _ = _split_content_and_comment(opt)

        assert tree_content == """    ○
[ ] └── Main Title
[ ]     ├── Introduction
        │   Brief introduction to the topic.
[ ]     │   └── Background
        │       Context or history relevant to the topic.
[ ]     │       └── Importance
        │           Why this topic matters in the current scenar
[ ]     │           └── Objective
        │               The primary goal of this document.
[ ]     ├── Methods
        │   Overview of the methodologies used.
[ ]     │   └── Data Collection
        │       How data was gathered for analysis.
[ ]     │       └── Tools Used
        │           List of tools utilized during the project.
[ ]     │           └── Future Work
        │               Suggestions for future research or tasks
[ ]     └── Conclusion
            Summarizing the findings and implications."""


# no content  ##################################################################
# w/ all args
class TestNoContent1:  # =======================================================

    def test_full(_, corpus_testee1):
        corpus = corpus_testee1
        bp_text = BLUEPRINT_1_FULL

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=0,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, comment_content = _split_content_and_comment(opt)

        assert tree_content == """    ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     └── License"""

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment_content)

    def test_part1(_, corpus_testee1):
        corpus = corpus_testee1
        bp_text = BLUEPRINT_1_PARTIAL_1

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=0,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, _ = _split_content_and_comment(opt)

        assert tree_content == """    ○
[ ] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     └── License"""

    def test_part2(_, corpus_testee1):
        corpus = corpus_testee1
        bp_text = BLUEPRINT_1_PARTIAL_2

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=0,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, _ = _split_content_and_comment(opt)

        assert tree_content == """    ○
[x] └── Project Title
[ ]     ├── Description
[x]     ├── Installation
[x]     └── License"""

    def test_empty(_, corpus_testee1):
        corpus = corpus_testee1
        bp_text = BLUEPRINT_1_EMPTY

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=0,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, _ = _split_content_and_comment(opt)

        assert tree_content == """    ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     └── License"""


class TestNoContent3:  # =======================================================

    def test_full(_, corpus_testee3):
        corpus = corpus_testee3
        bp_text = BLUEPRINT_3_FULL

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=0,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, comment_content = _split_content_and_comment(opt)

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

    def test_part1(_, corpus_testee3):
        corpus = corpus_testee3
        bp_text = BLUEPRINT_3_PARTIAL_1

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=0,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, _ = _split_content_and_comment(opt)

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

    def test_part2(_, corpus_testee3):
        corpus = corpus_testee3
        bp_text = BLUEPRINT_3_PARTIAL_2

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=0,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, _ = _split_content_and_comment(opt)

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

    def test_empty(_, corpus_testee3):
        corpus = corpus_testee3
        bp_text = BLUEPRINT_3_EMPTY

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=0,
            show_full_tree=False,
            show_comment=True,
        )

        print(opt)
        tree_content, _ = _split_content_and_comment(opt)

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


# no comment (nor content)  ####################################################
# w/ all args
class TestNoComment:  # =======================================================

    def test1(_, corpus_testee1):
        corpus = corpus_testee1
        bp_text = BLUEPRINT_1_FULL

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=0,
            show_full_tree=False,
            show_comment=False,
        )

        print(opt)
        assert opt == """    ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     └── License"""

    def test3(_, corpus_testee3):
        corpus = corpus_testee3
        bp_text = BLUEPRINT_3_FULL

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint(
            content_preview_lines=0,
            show_full_tree=False,
            show_comment=False,
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


# full tree (nor content)  #####################################################
class TestFullTree:

    def test1(_, bp_testee1pa2pruned):
        bp = bp_testee1pa2pruned

        opt = bp.generate_blueprint(
            content_preview_lines=0,
            show_full_tree=True,
            show_comment=False,
        )

        print(opt)

        assert opt == BLUEPRINT_1_PARTIAL_2

    def test2(_, corpus_testee2):
        bp_text = BLUEPRINT_2_PARTIAL_1_PRUNED
        bp = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee2)

        opt = bp.generate_blueprint(
            content_preview_lines=0,
            show_full_tree=True,
            show_comment=False,
        )

        print(opt)

        assert opt == BLUEPRINT_2_PARTIAL_1

    def test31(_, corpus_testee3):
        bp_text = BLUEPRINT_3_PARTIAL_1_PRUNED
        bp = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        opt = bp.generate_blueprint(
            content_preview_lines=0,
            show_full_tree=True,
            show_comment=False,
        )

        print(opt)

        assert opt == BLUEPRINT_3_PARTIAL_1

    def test32(_, corpus_testee3):
        bp_text = BLUEPRINT_3_PARTIAL_2_PRUNED
        bp = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        opt = bp.generate_blueprint(
            content_preview_lines=0,
            show_full_tree=True,
            show_comment=False,
        )

        print(opt)

        assert opt == BLUEPRINT_3_PARTIAL_2


# default  #####################################################################
class TestDft:

    def test1(_, corpus_testee1):
        corpus = corpus_testee1
        bp_text = BLUEPRINT_1_FULL

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint()

        print(opt)

        assert opt == BLUEPRINT_1_FULL_PREVIEW

    def test2(_, corpus_testee2):
        corpus = corpus_testee2
        bp_text = BLUEPRINT_2_FULL

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint()

        print(opt)

        assert opt == BLUEPRINT_2_PREVIEW

    def test3(_, corpus_testee3):
        corpus = corpus_testee3
        bp_text = BLUEPRINT_3_FULL

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = bp.generate_blueprint()

        print(opt)

        assert opt == BLUEPRINT_3_FULL_PREVIEW


class TestDynamicNodes:  #######################################################

    def test_abbr(_, dynamic_bp_testee1):
        opt = dynamic_bp_testee1.generate_blueprint(content_preview_lines=0)

        print(opt)

        assert opt == """    ○
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
