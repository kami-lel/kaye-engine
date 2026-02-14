"""
prompt-bp-contains_test.py

Unit Tests (using pytest) for: PromptBlueprint.__contains__()
"""

import pytest


from kaye.gen_prompt.prompt_blueprint import PromptBlueprint
from tests.prompt.bp import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_3_FULL,
)

# TODO unit test for dynamic node


# pytest fixures  ##############################################################
@pytest.fixture(scope="session")
def bp_testee1(corpus_testee1):
    return PromptBlueprint.parse(
        BLUEPRINT_1_FULL, disable_prune=True, corpus_override=corpus_testee1
    )


@pytest.fixture(scope="session")
def bp_testee3(corpus_testee3):
    return PromptBlueprint.parse(
        BLUEPRINT_3_FULL, disable_prune=True, corpus_override=corpus_testee3
    )


# node obj  ####################################################################
class TestObj1:  # =============================================================

    def test1(_, corpus_testee1, bp_testee1):
        proj_node = corpus_testee1.children[0]

        opt = proj_node in bp_testee1
        print(repr(opt) + "\t" + repr(proj_node))
        assert opt

    def test_description(_, corpus_testee1, bp_testee1):
        proj_node = corpus_testee1.children[0]
        _node = proj_node.children[0]
        opt = _node in bp_testee1
        print(repr(opt) + "\t" + repr(_node))
        assert opt

    def test_installation(_, corpus_testee1, bp_testee1):
        proj_node = corpus_testee1.children[0]
        _node = proj_node.children[1]
        opt = _node in bp_testee1
        print(repr(opt) + "\t" + repr(_node))
        assert opt

    def test_license(_, corpus_testee1, bp_testee1):
        proj_node = corpus_testee1.children[0]
        _node = proj_node.children[2]
        opt = _node in bp_testee1
        print(repr(opt) + "\t" + repr(_node))
        assert opt


class TestObj3:  # =============================================================

    def test1(_):
        pass


# hash  ########################################################################
class TestHash1:  # ============================================================

    def test1(_, corpus_testee1, bp_testee1):
        proj_node = corpus_testee1.children[0]

        opt = hash(proj_node) in bp_testee1
        print(repr(opt) + "\t" + repr(proj_node))
        assert opt

    def test_description(_, corpus_testee1, bp_testee1):
        proj_node = corpus_testee1.children[0]
        _node = proj_node.children[0]
        opt = hash(_node) in bp_testee1
        print(repr(opt) + "\t" + repr(_node))
        assert opt

    def test_installation(_, corpus_testee1, bp_testee1):
        proj_node = corpus_testee1.children[0]
        _node = proj_node.children[1]
        opt = hash(_node) in bp_testee1
        print(repr(opt) + "\t" + repr(_node))
        assert opt

    def test_license(_, corpus_testee1, bp_testee1):
        proj_node = corpus_testee1.children[0]
        _node = proj_node.children[2]
        opt = hash(_node) in bp_testee1
        print(repr(opt) + "\t" + repr(_node))
        assert opt


class TestHash3:  # ============================================================

    def test1(_):
        pass


class Test3:  # use corpus3  ##############################################

    # HACK HACK

    def test_full(_, corpus_testee3):
        bp_text = BLUEPRINT_3_FULL

        bp = PromptBlueprint.parse(
            bp_text,
            disable_prune=True,
            corpus_override=corpus_testee3,
        )

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus_testee3.children[0]
        opt = main_title_node in bp
        print(repr(opt) + "\t" + repr(main_title_node))
        assert opt

        # Introduction
        _node = main_title_node.children[0]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Background
        _node = _node.children[0]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Importance
        _node = _node.children[0]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Objective
        _node = _node.children[0]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Methods
        _node = main_title_node.children[1]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Data Collection
        _node = _node.children[0]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Tool Used
        _node = _node.children[0]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Future Work
        _node = _node.children[0]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Conclusion
        _node = main_title_node.children[2]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt
