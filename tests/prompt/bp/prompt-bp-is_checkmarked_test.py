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


class Test3Full:  # ============================================================

    def test1(_, corpus_testee3, bp_testee3full):
        corpus = corpus_testee3
        bp = bp_testee3full

        # main title
        main_title_node = corpus.children[0]
        opt = bp.is_checkmarked(main_title_node)
        print(repr(opt) + "\t" + repr(main_title_node))
        assert opt

    def test2(_, corpus_testee3, bp_testee3full):
        corpus = corpus_testee3
        bp = bp_testee3full

        # Introduction
        node = corpus.children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test3(_, corpus_testee3, bp_testee3full):
        corpus = corpus_testee3
        bp = bp_testee3full

        # Background
        node = corpus.children[0].children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test4(_, corpus_testee3, bp_testee3full):
        corpus = corpus_testee3
        bp = bp_testee3full

        # Importance
        node = corpus.children[0].children[0].children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test5(_, corpus_testee3, bp_testee3full):
        corpus = corpus_testee3
        bp = bp_testee3full

        # Objective
        node = (
            corpus.children[0].children[0].children[0].children[0].children[0]
        )
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test6(_, corpus_testee3, bp_testee3full):
        corpus = corpus_testee3
        bp = bp_testee3full

        # Methods
        node = corpus.children[0].children[1]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test7(_, corpus_testee3, bp_testee3full):
        corpus = corpus_testee3
        bp = bp_testee3full

        # Data Collection
        node = corpus.children[0].children[1].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test8(_, corpus_testee3, bp_testee3full):
        corpus = corpus_testee3
        bp = bp_testee3full

        # Tool Used
        node = corpus.children[0].children[1].children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test9(_, corpus_testee3, bp_testee3full):
        corpus = corpus_testee3
        bp = bp_testee3full

        # Future Work
        node = (
            corpus.children[0].children[1].children[0].children[0].children[0]
        )
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test10(_, corpus_testee3, bp_testee3full):
        corpus = corpus_testee3
        bp = bp_testee3full

        # Conclusion
        node = corpus.children[0].children[2]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt


class Test3Pa1:  # =============================================================

    def test1(_, corpus_testee3, bp_testee3pa1):
        corpus = corpus_testee3
        bp = bp_testee3pa1

        # main title
        main_title_node = corpus.children[0]
        opt = bp.is_checkmarked(main_title_node)
        print(repr(opt) + "\t" + repr(main_title_node))
        assert opt

    def test2(_, corpus_testee3, bp_testee3pa1):
        corpus = corpus_testee3
        bp = bp_testee3pa1

        # Introduction
        node = corpus.children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test3(_, corpus_testee3, bp_testee3pa1):
        corpus = corpus_testee3
        bp = bp_testee3pa1

        # Background
        node = corpus.children[0].children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test4(_, corpus_testee3, bp_testee3pa1):
        corpus = corpus_testee3
        bp = bp_testee3pa1

        # Importance
        node = corpus.children[0].children[0].children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test5(_, corpus_testee3, bp_testee3pa1):
        corpus = corpus_testee3
        bp = bp_testee3pa1

        # Objective
        node = (
            corpus.children[0].children[0].children[0].children[0].children[0]
        )
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test6(_, corpus_testee3, bp_testee3pa1):
        corpus = corpus_testee3
        bp = bp_testee3pa1

        # Methods
        node = corpus.children[0].children[1]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test7(_, corpus_testee3, bp_testee3pa1):
        corpus = corpus_testee3
        bp = bp_testee3pa1

        # Data Collection
        node = corpus.children[0].children[1].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test8(_, corpus_testee3, bp_testee3pa1):
        corpus = corpus_testee3
        bp = bp_testee3pa1

        # Tool Used
        node = corpus.children[0].children[1].children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test9(_, corpus_testee3, bp_testee3pa1):
        corpus = corpus_testee3
        bp = bp_testee3pa1

        # Future Work
        node = (
            corpus.children[0].children[1].children[0].children[0].children[0]
        )
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test10(_, corpus_testee3, bp_testee3pa1):
        corpus = corpus_testee3
        bp = bp_testee3pa1

        # Conclusion
        node = corpus.children[0].children[2]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt


class Test3Pa2:  # =============================================================

    def test1(_, corpus_testee3, bp_testee3pa2):
        corpus = corpus_testee3
        bp = bp_testee3pa2

        # main title
        main_title_node = corpus.children[0]
        opt = bp.is_checkmarked(main_title_node)
        print(repr(opt) + "\t" + repr(main_title_node))
        assert opt

    def test2(_, corpus_testee3, bp_testee3pa2):
        corpus = corpus_testee3
        bp = bp_testee3pa2

        # Introduction
        node = corpus.children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test3(_, corpus_testee3, bp_testee3pa2):
        corpus = corpus_testee3
        bp = bp_testee3pa2

        # Background
        node = corpus.children[0].children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test4(_, corpus_testee3, bp_testee3pa2):
        corpus = corpus_testee3
        bp = bp_testee3pa2

        # Importance
        node = corpus.children[0].children[0].children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test5(_, corpus_testee3, bp_testee3pa2):
        corpus = corpus_testee3
        bp = bp_testee3pa2

        # Objective
        node = (
            corpus.children[0].children[0].children[0].children[0].children[0]
        )
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test6(_, corpus_testee3, bp_testee3pa2):
        corpus = corpus_testee3
        bp = bp_testee3pa2

        # Methods
        node = corpus.children[0].children[1]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test7(_, corpus_testee3, bp_testee3pa2):
        corpus = corpus_testee3
        bp = bp_testee3pa2

        # Data Collection
        node = corpus.children[0].children[1].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test8(_, corpus_testee3, bp_testee3pa2):
        corpus = corpus_testee3
        bp = bp_testee3pa2

        # Tool Used
        node = corpus.children[0].children[1].children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test9(_, corpus_testee3, bp_testee3pa2):
        corpus = corpus_testee3
        bp = bp_testee3pa2

        # Future Work
        node = (
            corpus.children[0].children[1].children[0].children[0].children[0]
        )
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test10(_, corpus_testee3, bp_testee3pa2):
        corpus = corpus_testee3
        bp = bp_testee3pa2

        # Conclusion
        node = corpus.children[0].children[2]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt


class Test3Empty:  # ===========================================================

    def test1(_, corpus_testee3, bp_testee3empty):
        corpus = corpus_testee3
        bp = bp_testee3empty

        # main title
        main_title_node = corpus.children[0]
        opt = bp.is_checkmarked(main_title_node)
        print(repr(opt) + "\t" + repr(main_title_node))
        assert not opt

    def test2(_, corpus_testee3, bp_testee3empty):
        corpus = corpus_testee3
        bp = bp_testee3empty

        # Introduction
        node = corpus.children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test3(_, corpus_testee3, bp_testee3empty):
        corpus = corpus_testee3
        bp = bp_testee3empty

        # Background
        node = corpus.children[0].children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test4(_, corpus_testee3, bp_testee3empty):
        corpus = corpus_testee3
        bp = bp_testee3empty

        # Importance
        node = corpus.children[0].children[0].children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test5(_, corpus_testee3, bp_testee3empty):
        corpus = corpus_testee3
        bp = bp_testee3empty

        # Objective
        node = (
            corpus.children[0].children[0].children[0].children[0].children[0]
        )
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test6(_, corpus_testee3, bp_testee3empty):
        corpus = corpus_testee3
        bp = bp_testee3empty

        # Methods
        node = corpus.children[0].children[1]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test7(_, corpus_testee3, bp_testee3empty):
        corpus = corpus_testee3
        bp = bp_testee3empty

        # Data Collection
        node = corpus.children[0].children[1].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test8(_, corpus_testee3, bp_testee3empty):
        corpus = corpus_testee3
        bp = bp_testee3empty

        # Tool Used
        node = corpus.children[0].children[1].children[0].children[0]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test9(_, corpus_testee3, bp_testee3empty):
        corpus = corpus_testee3
        bp = bp_testee3empty

        # Future Work
        node = (
            corpus.children[0].children[1].children[0].children[0].children[0]
        )
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
        assert not opt

    def test10(_, corpus_testee3, bp_testee3empty):
        corpus = corpus_testee3
        bp = bp_testee3empty

        # Conclusion
        node = corpus.children[0].children[2]
        opt = bp.is_checkmarked(node)
        print(repr(opt) + "\t" + repr(node))
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
