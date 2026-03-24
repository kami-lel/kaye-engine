"""
promo 'Search Highlight OFF't-bp-contains_test.py

Unit Tests (using pytest) for: PromptBlueprint.__contains__()
"""

import copy


import pytest


from kaye.prompt.prompt_blueprint import PromptBlueprint
from tests.prompt.bp import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_3_FULL,
)


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


# prompt 1  ####################################################################
class TestObj1:  # =============================================================

    def test_project(_, corpus_testee1, bp_testee1):
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


class TestHash1:  # ============================================================

    def test_project(_, corpus_testee1, bp_testee1):
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


class TestName1:  # ============================================================

    def test_project(_, bp_testee1):
        key = "Project Title"

        opt = key in bp_testee1
        print(repr(opt) + "\t" + repr(key))
        assert opt

    def test_description(_, bp_testee1):
        key = "Description"

        opt = key in bp_testee1
        print(repr(opt) + "\t" + repr(key))
        assert opt

    def test_installation(_, bp_testee1):
        key = "Installation"

        opt = key in bp_testee1

        print(repr(opt) + "\t" + repr(key))
        assert opt

    def test_license(_, bp_testee1):
        key = "License"

        opt = key in bp_testee1

        print(repr(opt) + "\t" + repr(key))
        assert opt


# prompt 3  ####################################################################
class TestObj3:  # =============================================================

    def test_main(_, corpus_testee3, bp_testee3):
        node = corpus_testee3.children[0]
        opt = node in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_introduction(_, corpus_testee3, bp_testee3):
        main_title_node = corpus_testee3.children[0]
        node = main_title_node.children[0]
        opt = node in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_background(_, corpus_testee3, bp_testee3):
        node = corpus_testee3.children[0].children[0].children[0]
        opt = node in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_importance(_, corpus_testee3, bp_testee3):
        node = corpus_testee3.children[0].children[0].children[0].children[0]
        opt = node in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_objective(_, corpus_testee3, bp_testee3):
        node = (
            corpus_testee3.children[0]
            .children[0]
            .children[0]
            .children[0]
            .children[0]
        )
        opt = node in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_methods(_, corpus_testee3, bp_testee3):
        node = corpus_testee3.children[0].children[1]
        opt = node in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_data_collection(_, corpus_testee3, bp_testee3):
        node = corpus_testee3.children[0].children[1].children[0]
        opt = node in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_tools_used(_, corpus_testee3, bp_testee3):
        node = corpus_testee3.children[0].children[1].children[0].children[0]
        opt = node in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_future_work(_, corpus_testee3, bp_testee3):
        node = (
            corpus_testee3.children[0]
            .children[1]
            .children[0]
            .children[0]
            .children[0]
        )
        opt = node in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_conclusion(_, corpus_testee3, bp_testee3):
        node = corpus_testee3.children[0].children[2]
        opt = node in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt


class TestHash3:  # ============================================================

    def test_main(_, corpus_testee3, bp_testee3):
        node = corpus_testee3.children[0]
        opt = hash(node) in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_introduction(_, corpus_testee3, bp_testee3):
        main_title_node = corpus_testee3.children[0]
        node = main_title_node.children[0]
        opt = hash(node) in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_background(_, corpus_testee3, bp_testee3):
        node = corpus_testee3.children[0].children[0].children[0]
        opt = hash(node) in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_importance(_, corpus_testee3, bp_testee3):
        node = corpus_testee3.children[0].children[0].children[0].children[0]
        opt = hash(node) in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_objective(_, corpus_testee3, bp_testee3):
        node = (
            corpus_testee3.children[0]
            .children[0]
            .children[0]
            .children[0]
            .children[0]
        )
        opt = hash(node) in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_methods(_, corpus_testee3, bp_testee3):
        node = corpus_testee3.children[0].children[1]
        opt = hash(node) in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_data_collection(_, corpus_testee3, bp_testee3):
        node = corpus_testee3.children[0].children[1].children[0]
        opt = hash(node) in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_tools_used(_, corpus_testee3, bp_testee3):
        node = corpus_testee3.children[0].children[1].children[0].children[0]
        opt = hash(node) in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_future_work(_, corpus_testee3, bp_testee3):
        node = (
            corpus_testee3.children[0]
            .children[1]
            .children[0]
            .children[0]
            .children[0]
        )
        opt = hash(node) in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt

    def test_conclusion(_, corpus_testee3, bp_testee3):
        node = corpus_testee3.children[0].children[2]
        opt = hash(node) in bp_testee3
        print(repr(opt) + "\t" + repr(node))
        assert opt


class TestName3:  # ============================================================

    def test_main(_, bp_testee3):
        key = "Main Title"

        opt = key in bp_testee3

        print(repr(opt) + "\t" + repr(key))
        assert opt

    def test_introduction(_, bp_testee3):
        key = "Introduction"

        opt = key in bp_testee3

        print(repr(opt) + "\t" + repr(key))
        assert opt

    def test_background(_, bp_testee3):
        key = "Background"

        opt = key in bp_testee3

        print(repr(opt) + "\t" + repr(key))
        assert opt

    def test_importance(_, bp_testee3):
        key = "Importance"

        opt = key in bp_testee3

        print(repr(opt) + "\t" + repr(key))
        assert opt

    def test_objective(_, bp_testee3):
        key = "Objective"

        opt = key in bp_testee3

        print(repr(opt) + "\t" + repr(key))
        assert opt

    def test_methods(_, bp_testee3):
        key = "Methods"

        opt = key in bp_testee3

        print(repr(opt) + "\t" + repr(key))
        assert opt

    def test_data_collection(_, bp_testee3):
        key = "Data Collection"

        opt = key in bp_testee3

        print(repr(opt) + "\t" + repr(key))
        assert opt

    def test_tools_used(_, bp_testee3):
        key = "Tools Used"

        opt = key in bp_testee3

        print(repr(opt) + "\t" + repr(key))
        assert opt

    def test_future_work(_, bp_testee3):
        key = "Future Work"

        opt = key in bp_testee3
        print(repr(opt) + "\t" + repr(key))
        assert opt

    def test_conclusion(_, bp_testee3):
        key = "Conclusion"

        opt = key in bp_testee3

        print(repr(opt) + "\t" + repr(key))
        assert opt


class TestDynamicNodes:  #######################################################

    def test_obj1(_, dynamic_bp_testee1):
        bp = copy.deepcopy(dynamic_bp_testee1)

        node = dynamic_bp_testee1.corpus["Main Title"]["Methods"][
            "{Programming Languages Code}"
        ]

        assert node in bp

    def test_hash1(_, dynamic_bp_testee1):
        bp = copy.deepcopy(dynamic_bp_testee1)

        node = dynamic_bp_testee1.corpus["Main Title"]["Methods"][
            "{Programming Languages Code}"
        ]

        assert hash(node) in bp

    def test_name1(_, dynamic_bp_testee1):
        bp = copy.deepcopy(dynamic_bp_testee1)

        assert "{Programming Languages Code}" in bp

    def test_id1(_, dynamic_bp_testee1):
        bp = copy.deepcopy(dynamic_bp_testee1)

        assert "{Programming Languages Code}" in bp
