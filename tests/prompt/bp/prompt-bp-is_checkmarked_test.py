"""
prompt-bp-is_checkmarked_test.py

Unit Tests (using pytest) for: PromptBlueprint.is_checkmarked()
"""

import copy


import pytest


from kaye.prompt import PromptBlueprint
from tests.prompt.bp import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_1_EMPTY,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_2,
    BLUEPRINT_3_EMPTY,
)


# use corpus 1  ################################################################
# pytest fixtures  =============================================================
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
def bp_testee1empty(corpus_testee1):
    corpus = corpus_testee1
    return PromptBlueprint.parse(
        BLUEPRINT_1_EMPTY, disable_prune=True, corpus_override=corpus
    )


class Test1Full:  # ============================================================

    def test_proj(_, corpus_testee1, bp_testee1full):
        bp = bp_testee1full
        corpus = corpus_testee1
        proj_node = corpus.children[0]

        opt = bp.is_checkmarked(proj_node)
        print(repr(opt) + "\t" + repr(proj_node))
        assert opt

    def test_description(_, corpus_testee1, bp_testee1full):
        bp = bp_testee1full
        corpus = corpus_testee1
        node = corpus.children[0].children[0]

        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_installation(_, corpus_testee1, bp_testee1full):
        bp = bp_testee1full
        corpus = corpus_testee1
        node = corpus.children[0].children[1]

        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_license(_, corpus_testee1, bp_testee1full):
        bp = bp_testee1full
        corpus = corpus_testee1
        node = corpus.children[0].children[2]

        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    # special cases  -----------------------------------------------------------

    def test_not_contained1(_, corpus_testee3, bp_testee1full):
        # a node that is not contained in bp at all
        bp = bp_testee1full
        assert not bp.is_checkmarked(corpus_testee3)

    def test_not_contained2(_, corpus_testee3, bp_testee1full):
        # a node that is not contained in bp at all
        bp = bp_testee1full
        assert not bp.is_checkmarked(corpus_testee3.children[0])


class Test1Pa1:  # =============================================================

    def test_proj(_, corpus_testee1, bp_testee1pa1):
        bp = bp_testee1pa1
        corpus = corpus_testee1
        proj_node = corpus.children[0]

        opt = bp.is_checkmarked(proj_node)
        print(repr(opt) + "\t" + repr(proj_node))
        assert not opt

    def test_description(_, corpus_testee1, bp_testee1pa1):
        bp = bp_testee1pa1
        corpus = corpus_testee1
        node = corpus.children[0].children[0]

        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_installation(_, corpus_testee1, bp_testee1pa1):
        bp = bp_testee1pa1
        corpus = corpus_testee1
        node = corpus.children[0].children[1]

        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_license(_, corpus_testee1, bp_testee1pa1):
        bp = bp_testee1pa1
        corpus = corpus_testee1
        node = corpus.children[0].children[2]

        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt


class Test1Pa2:  # =============================================================

    def test_proj(_, corpus_testee1, bp_testee1pa2):
        bp = bp_testee1pa2
        corpus = corpus_testee1
        proj_node = corpus.children[0]

        opt = bp.is_checkmarked(proj_node)
        print(repr(opt) + "\t" + repr(proj_node))
        assert opt

    def test_description(_, corpus_testee1, bp_testee1pa2):
        bp = bp_testee1pa2
        corpus = corpus_testee1
        node = corpus.children[0].children[0]

        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test_installation(_, corpus_testee1, bp_testee1pa2):
        bp = bp_testee1pa2
        corpus = corpus_testee1
        node = corpus.children[0].children[1]

        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_license(_, corpus_testee1, bp_testee1pa2):
        bp = bp_testee1pa2
        corpus = corpus_testee1
        node = corpus.children[0].children[2]

        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt


class Test1Empty:  # ===========================================================

    def test_proj(_, corpus_testee1, bp_testee1empty):
        bp = bp_testee1empty
        corpus = corpus_testee1
        proj_node = corpus.children[0]

        opt = bp.is_checkmarked(proj_node)
        print(repr(opt) + "\t" + repr(proj_node))
        assert not opt

    def test_description(_, corpus_testee1, bp_testee1empty):
        bp = bp_testee1empty
        corpus = corpus_testee1
        node = corpus.children[0].children[0]

        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test_installation(_, corpus_testee1, bp_testee1empty):
        bp = bp_testee1empty
        corpus = corpus_testee1
        node = corpus.children[0].children[1]

        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test_license(_, corpus_testee1, bp_testee1empty):
        bp = bp_testee1empty
        corpus = corpus_testee1
        node = corpus.children[0].children[2]

        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt


# use corpus 3  ################################################################
# pytest fixtures  =============================================================

# use dynamic nodes  ###########################################################


# HACK rm these


class Test3:  # use corpus3  ##################################################

    def test_full(_, corpus_testee3):
        corpus = corpus_testee3
        bp_text = BLUEPRINT_3_FULL

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        opt = bp.is_checkmarked(main_title_node)
        print(repr(opt) + "\t" + repr(main_title_node))
        assert opt

        # Introduction
        _node = main_title_node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Background
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Importance
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Objective
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Methods
        _node = main_title_node.children[1]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Data Collection
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Tool Used
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Future Work
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Conclusion
        _node = main_title_node.children[2]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

    def test_part1(_, corpus_testee3):
        corpus = corpus_testee3
        bp_text = BLUEPRINT_3_PARTIAL_1

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        opt = bp.is_checkmarked(main_title_node)
        print(repr(opt) + "\t" + repr(main_title_node))
        assert opt

        # Introduction
        _node = main_title_node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Background
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Importance
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Objective
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Methods
        _node = main_title_node.children[1]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Data Collection
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Tool Used
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Future Work
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Conclusion
        _node = main_title_node.children[2]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

    def test_part2(_, corpus_testee3):
        corpus = corpus_testee3
        bp_text = BLUEPRINT_3_PARTIAL_2
        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )

        print(bp)
        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        opt = bp.is_checkmarked(main_title_node)
        print(repr(opt) + "\t" + repr(main_title_node))
        assert opt

        # Introduction
        _node = main_title_node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Background
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Importance
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Objective
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Methods
        _node = main_title_node.children[1]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Data Collection
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Tool Used
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Future Work
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Conclusion
        _node = main_title_node.children[2]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

    def test_empty(_, corpus_testee3):
        corpus = corpus_testee3

        bp_text = BLUEPRINT_3_EMPTY
        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )

        print(bp)
        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        opt = bp.is_checkmarked(main_title_node)
        print(repr(opt) + "\t" + repr(main_title_node))
        assert not opt

        # Introduction
        _node = main_title_node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Background
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Importance
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Objective
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Methods
        _node = main_title_node.children[1]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Data Collection
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Tool Used
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Future Work
        _node = _node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # Conclusion
        _node = main_title_node.children[2]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt


class TestDynamicNodes:  #######################################################

    def test_abbr(_, dynamic_bp_testee1):
        bp = copy.deepcopy(dynamic_bp_testee1)

        node = dynamic_bp_testee1.corpus["Main Title"]["Introduction"][
            "Background"
        ]["Importance"]["Abbreviations"]

        assert bp.is_checkmarked(node)

    def test_plc(_, dynamic_bp_testee1):
        bp = copy.deepcopy(dynamic_bp_testee1)

        node = dynamic_bp_testee1.corpus["Main Title"]["Methods"][
            "Programming Languages Code"
        ]

        assert not bp.is_checkmarked(node)
