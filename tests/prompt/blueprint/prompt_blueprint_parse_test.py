"""
prompt_blueprint_parse_basic_test.py

Unit Tests (using pytest) for: PromptBlueprint.parse()
"""

import pytest


from kaye.gen_prompt import PromptCorpusNode, PromptBlueprint

from tests.prompt import PROMPT1, PROMPT2, PROMPT3
from tests.prompt.blueprint import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_FULL_PREVIEW,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_1_PREVIEW,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_1_PARTIAL_2_PREVIEW,
    BLUEPRINT_1_PARTIAL_2_PRUNED,
    BLUEPRINT_1_EMPTY,
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
    BLUEPRINT_EMPTY_PRUNED,
)

CORPUS1 = PromptCorpusNode.parse(PROMPT1)
CORPUS2 = PromptCorpusNode.parse(PROMPT2)
CORPUS3 = PromptCorpusNode.parse(PROMPT3)


# basic  #######################################################################
class TestBasic1:  # use corpus1  ==============================================

    def test_full(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_FULL

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 4
        assert opt.corpus is corpus
        assert opt.display_name == ""

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        _hash = hash(proj_node)
        assert _hash in opt
        assert opt[_hash]

        # test Description
        _node = proj_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # test Installation
        _node = proj_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # test License
        _node = proj_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

    def test_no_project(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_PARTIAL_1

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 4

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        _hash = hash(proj_node)
        assert _hash in opt
        assert not opt[_hash]

        # test Description
        _node = proj_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # test Installation
        _node = proj_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # test License
        _node = proj_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

    def test_no_description(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_PARTIAL_2

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 4

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        _hash = hash(proj_node)
        assert _hash in opt
        assert opt[_hash]

        # test Description
        _node = proj_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # test Installation
        _node = proj_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # test License
        _node = proj_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

    def test_empty(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_EMPTY

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 4

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        _hash = hash(proj_node)
        assert _hash in opt
        assert not opt[_hash]

        # test Description
        _node = proj_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # test Installation
        _node = proj_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # test License
        _node = proj_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]


class TestBasic3:  # use corpus3  ==============================================

    def test_full(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_FULL

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 10
        assert opt.corpus is corpus
        assert opt.display_name == ""

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        _hash = hash(main_title_node)
        assert _hash in opt
        assert opt[_hash]

        # Introduction
        _node = main_title_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Background
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Importance
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Objective
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Methods
        _node = main_title_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Data Collection
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Tool Used
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Future Work
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Conclusion
        _node = main_title_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

    def test_part1(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_PARTIAL_1

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 10

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        _hash = hash(main_title_node)
        assert _hash in opt
        assert opt[_hash]

        # Introduction
        _node = main_title_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Background
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Importance
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Objective
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Methods
        _node = main_title_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Data Collection
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Tool Used
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Future Work
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Conclusion
        _node = main_title_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

    def test_part2(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_PARTIAL_2
        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 10

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        _hash = hash(main_title_node)
        assert _hash in opt
        assert opt[_hash]

        # Introduction
        _node = main_title_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Background
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Importance
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Objective
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Methods
        _node = main_title_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Data Collection
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Tool Used
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Future Work
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Conclusion
        _node = main_title_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

    def test_empty(_):
        corpus = CORPUS3

        bp_text = BLUEPRINT_3_EMPTY
        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 10

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        _hash = hash(main_title_node)
        assert _hash in opt
        assert not opt[_hash]

        # Introduction
        _node = main_title_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Background
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Importance
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Objective
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Methods
        _node = main_title_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Data Collection
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Tool Used
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Future Work
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Conclusion
        _node = main_title_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]


# setting display_name  ########################################################


class TestDisplayName:

    def test_dft(_):
        bp_text = BLUEPRINT_1_FULL

        opt = PromptBlueprint.parse(CORPUS1, bp_text)

        print(opt)
        assert opt.display_name == ""

    def test1(_):
        bp_text = BLUEPRINT_1_FULL
        display_name = "My Blueprint"

        opt = PromptBlueprint.parse(
            CORPUS1, bp_text, display_name=display_name
        )

        print(opt)
        assert opt.display_name == display_name

    def test2(_):
        bp_text = BLUEPRINT_1_PARTIAL_1
        display_name = "My Blueprint"

        opt = PromptBlueprint.parse(
            CORPUS1, bp_text, display_name=display_name
        )

        print(opt)
        assert opt.display_name == display_name

    def test3(_):
        bp_text = BLUEPRINT_3_EMPTY
        display_name = "My Blueprint"

        opt = PromptBlueprint.parse(
            CORPUS3, bp_text, display_name=display_name
        )

        print(opt)
        assert opt.display_name == display_name


# err handling  ################################################################


class TestErr:

    def test_malformed(_):
        bp_text = """    ○
[ ] └── Project Title
[x]     ├── Description
[x]         ├── Installation
[x]     └── License"""

        with pytest.raises(ValueError) as exec_info:
            PromptBlueprint.parse(CORPUS1, bp_text)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == """missing node from prompt_corpus:
[x]         ├── Installation"""

    def test_missing_node(_):
        bp_text = """    ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Node Nonexistent In Prompt
[x]     ├── Installation
[x]     └── License"""

        with pytest.raises(ValueError) as exec_info:
            PromptBlueprint.parse(CORPUS1, bp_text)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == """missing node from prompt_corpus:
[x]     ├── Node Nonexistent In Prompt"""


# default behavior  ############################################################
class TestDft1:  # use PROMPT1  ==============================================

    corpus = CORPUS1

    def test_full(self):
        bp_text = BLUEPRINT_1_FULL

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 4
        assert opt.corpus is self.corpus
        assert opt.display_name == ""
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test_part1(self):
        bp_text = BLUEPRINT_1_PARTIAL_1

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 4
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test_part2(self):
        bp_text = BLUEPRINT_1_PARTIAL_2

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 3
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_2_PRUNED
        )

    def test_empty(self):
        bp_text = BLUEPRINT_1_EMPTY

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 0
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_EMPTY_PRUNED
        )


class TestDft2:  # use PROMPT2  ================================================

    corpus = CORPUS2

    def test_full(self):
        bp_text = BLUEPRINT_2_FULL

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 6
        assert opt.corpus is self.corpus
        assert opt.display_name == ""
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test_part1(self):
        bp_text = BLUEPRINT_2_PARTIAL_1

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 3
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_2_PARTIAL_1_PRUNED
        )

    def test_empty(self):
        bp_text = BLUEPRINT_2_EMPTY

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 0
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_EMPTY_PRUNED
        )


class TestDft3:  # use PROMPT3  ================================================

    corpus = CORPUS3

    def test_full(self):
        bp_text = BLUEPRINT_3_FULL

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 10
        assert opt.corpus is self.corpus
        assert opt.display_name == ""
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test_part1(self):
        bp_text = BLUEPRINT_3_PARTIAL_1

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 6
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_1_PRUNED
        )

    def test_part2(self):
        bp_text = BLUEPRINT_3_PARTIAL_2
        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 9
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_2_PRUNED
        )

    def test_empty(self):
        bp_text = BLUEPRINT_3_EMPTY
        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 0
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_EMPTY_PRUNED
        )


# text include content preview  ################################################
class TestContentPreview1:  # use PROMPT1  =====================================

    def test1(_):
        bp_text = BLUEPRINT_1_FULL_PREVIEW

        opt = PromptBlueprint.parse(CORPUS1, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_FULL
        )

    def test_pa1(_):
        bp_text = BLUEPRINT_1_PARTIAL_1_PREVIEW

        opt = PromptBlueprint.parse(CORPUS1, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_1
        )

    def test_pa2(_):
        bp_text = BLUEPRINT_1_PARTIAL_2_PREVIEW

        opt = PromptBlueprint.parse(CORPUS1, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_2_PRUNED
        )


class TestContentPreview2:  # use PROMPT2  =====================================

    def test_full(_):
        bp_text = BLUEPRINT_2_PREVIEW

        opt = PromptBlueprint.parse(CORPUS2, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_2_FULL
        )

    def test_pa1(_):
        bp_text = BLUEPRINT_2_PARTIAL_1_PREVIEW

        opt = PromptBlueprint.parse(CORPUS2, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_2_PARTIAL_1_PRUNED
        )


class TestContentPreview3:  # use PROMPT2  =====================================

    def test_full(_):
        bp_text = BLUEPRINT_3_FULL_PREVIEW

        opt = PromptBlueprint.parse(CORPUS3, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_FULL
        )

    def test_pa1(_):
        bp_text = BLUEPRINT_3_PARTIAL_1_PREVIEW

        opt = PromptBlueprint.parse(CORPUS3, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_1_PRUNED
        )

    def test_pa2(_):
        bp_text = BLUEPRINT_3_PARTIAL_2_PREVIEW

        opt = PromptBlueprint.parse(CORPUS3, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_2_PRUNED
        )


# blueprint text is pruned  ####################################################
class TestPrunedText:

    def test1(_):
        bp_text = BLUEPRINT_1_PARTIAL_2_PRUNED

        opt = PromptBlueprint.parse(CORPUS1, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test2(_):
        bp_text = BLUEPRINT_2_PARTIAL_1_PRUNED

        opt = PromptBlueprint.parse(CORPUS2, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test31(_):
        bp_text = BLUEPRINT_3_PARTIAL_1_PRUNED

        opt = PromptBlueprint.parse(CORPUS3, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test32(_):
        bp_text = BLUEPRINT_3_PARTIAL_2_PRUNED

        opt = PromptBlueprint.parse(CORPUS3, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test_pruned_input(_):
        bp_text = """    ○
[x] └── Main Title
[x]     ├── Introduction
        │   Brief introduction to the topic.
[x]     │   └── Background
        │       Context or history relevant to the topic.
[x]     │       └── Importance
        │           Why this topic matters in the current scenario.
[x]     │           └── Objective
        │               The primary goal of this document.
[x]     └── Conclusion
            Summarizing the findings and implications."""

        opt = PromptBlueprint.parse(CORPUS3, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_1_PRUNED
        )
