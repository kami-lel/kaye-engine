"""
prompt-bp-checkmark_test.py

Unit Tests (using pytest) for: PromptBlueprint:

- .checkmark()
- .__iadd__()
"""

import copy


import pytest

from tests.prompt.bp import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_2_FULL,
    BLUEPRINT_3_FULL,
)


# pytest fixtures  #############################################################
@pytest.fixture
def local_testee11(bp_testee1pa1):
    return copy.deepcopy(bp_testee1pa1), BLUEPRINT_1_FULL


@pytest.fixture
def local_testee12(bp_testee1pa2):
    return copy.deepcopy(bp_testee1pa2), BLUEPRINT_1_FULL


@pytest.fixture
def local_testee2(bp_testee2pa1):
    return copy.deepcopy(bp_testee2pa1), BLUEPRINT_2_FULL


@pytest.fixture
def local_testee31(bp_testee3pa1):
    return copy.deepcopy(bp_testee3pa1), BLUEPRINT_3_FULL


@pytest.fixture
def local_testee32(bp_testee3pa2):
    return copy.deepcopy(bp_testee3pa2), BLUEPRINT_3_FULL


@pytest.fixture
def local_dynamic_testee1(dynamic_bp_testee1):
    return copy.deepcopy(dynamic_bp_testee1)


# tests on prompt 1  ###########################################################
class Test11:  # ===============================================================

    # test .checkmark()  *******************************************************

    def test_checkmark_by_obj1(_, corpus_testee1, local_testee11):
        bp, answer = local_testee11

        print(repr(bp))
        node = corpus_testee1["Project Title"]

        bp.checkmark(node)

        print("#" * 80)
        print(repr(bp))

        assert (
            bp.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    def test_checkmark_by_hash1(_, corpus_testee1, local_testee11):
        bp, answer = local_testee11

        print(repr(bp))
        node = corpus_testee1["Project Title"]
        node_hash = hash(node)

        bp.checkmark(node_hash)

        print("#" * 80)
        print(repr(bp))

        assert (
            bp.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    def test_checkmark_by_name1(_, corpus_testee1, local_testee11):
        bp, answer = local_testee11

        print(repr(bp))

        bp.checkmark("Project Title")

        print("#" * 80)
        print(repr(bp))

        assert (
            bp.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    # test +=  *****************************************************************

    def test_iadd_by_obj1(_, corpus_testee1, local_testee11):
        bp, answer = local_testee11

        print(repr(bp))
        node = corpus_testee1["Project Title"]

        bp += node

        print("#" * 80)
        print(repr(bp))

        assert (
            bp.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    def test_iadd_by_hash1(_, corpus_testee1, local_testee11):
        bp, answer = local_testee11

        print(repr(bp))
        node = corpus_testee1["Project Title"]
        node_hash = hash(node)

        bp += node_hash

        print("#" * 80)
        print(repr(bp))

        assert (
            bp.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    def test_iadd_by_name1(_, local_testee11):
        bp, answer = local_testee11

        print(repr(bp))

        bp += "Project Title"

        print("#" * 80)
        print(repr(bp))

        assert (
            bp.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    # err handling  ************************************************************
    def test_bad_type1(_, local_testee11):
        bp, _ = local_testee11
        ipt = 12.5

        with pytest.raises(TypeError) as exec_info:
            bp.checkmark(ipt)

        opt = exec_info.value.args[0]
        print(opt)

        assert (
            opt
            == "must be BasePromptNode/"
            "int(hash value)/str(name/identifier): 12.5"
        )

    def test_bad_type2(_, local_testee11):
        bp, _ = local_testee11
        ipt = ["a", "b", "c"]

        with pytest.raises(TypeError) as exec_info:
            bp.checkmark(ipt)

        opt = exec_info.value.args[0]
        print(opt)

        assert (
            opt
            == "must be BasePromptNode/"
            "int(hash value)/str(name/identifier): ['a', 'b', 'c']"
        )

    def test_bad_str_no_found1(_, local_testee11):
        bp, _ = local_testee11
        ipt = "AAAZZZ"

        with pytest.raises(ValueError) as exec_info:
            bp.checkmark(ipt)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "no node in corpus with name/identifier: 'AAAZZZ'"

    def test_bad_hash(self, local_testee11):
        bp, _ = local_testee11

        with pytest.raises(ValueError) as exec_info:
            bp.checkmark(5)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "no node in corpus with hash value: 5"

    def test_bad_obj(self, local_testee11, corpus_testee3):
        bp, _ = local_testee11
        bad_node = corpus_testee3.children[0]

        with pytest.raises(ValueError) as exec_info:
            bp.checkmark(bad_node)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "node not in corpus: PromptCorpusNode(Main Title)"


class Test12:  # ===============================================================

    def test2_checkmark_by_obj(_, local_testee12, corpus_testee1):
        bp, answer = local_testee12

        print(bp)

        node = corpus_testee1["Project Title"]["Description"]
        bp.checkmark(node)

        print("#" * 80)
        print(bp)

        assert (
            bp.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    def test2_checkmark_by_hash(_, local_testee12, corpus_testee1):
        bp, answer = local_testee12

        print(bp)

        node = corpus_testee1["Project Title"]["Description"]
        node_hash = hash(node)
        bp.checkmark(node_hash)

        print("#" * 80)
        print(bp)

        assert (
            bp.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )


class Test2:  # tests on prompt 2  ############################################
    def test1_checkmark_by_obj(_, corpus_testee2, local_testee2):
        bp, answer = local_testee2
        print(bp)

        proj_node = corpus_testee2["Project Title"]
        bp.checkmark(proj_node["Description"]).checkmark(
            proj_node["Usage"]
        ).checkmark(proj_node["License"])

        print("#" * 80)
        print(bp)

        assert (
            bp.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    def test1_checkmark_by_hash(_, corpus_testee2, local_testee2):
        bp, answer = local_testee2
        print(bp)

        proj_node = corpus_testee2["Project Title"]
        for h in [
            hash(proj_node[name])
            for name in ("Description", "Usage", "License")
        ]:
            bp.checkmark(h)

        print("#" * 80)
        print(bp)

        assert (
            bp.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )


# tests on prompt 3  ###########################################################
class Test31:  # ===============================================================

    def test1_checkmark_by_obj(_, corpus_testee3, local_testee31):
        opt, answer = local_testee31
        print(opt)

        node = corpus_testee3["Main Title"]["Methods"]
        opt.checkmark(node)
        node = node["Data Collection"]
        opt.checkmark(node)
        node = node["Tools Used"]
        opt.checkmark(node)
        node = node["Future Work"]
        opt.checkmark(node)

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    def test1_checkmark_by_hash(_, corpus_testee3, local_testee31):
        opt, answer = local_testee31
        print(opt)

        node = corpus_testee3["Main Title"]["Methods"]
        opt.checkmark(hash(node))
        node = node["Data Collection"]
        opt.checkmark(hash(node))
        node = node["Tools Used"]
        opt.checkmark(hash(node))
        node = node["Future Work"]
        opt.checkmark(hash(node))

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )


class Test32:  # ===============================================================

    def test2_checkmark_by_obj(_, corpus_testee3, local_testee32):
        opt, answer = local_testee32

        print(opt)

        main_node = corpus_testee3["Main Title"]
        node = main_node["Introduction"]
        opt.checkmark(node)
        node = node["Background"]["Importance"]
        opt.checkmark(node)
        node = main_node["Methods"]
        opt.checkmark(node)
        node = node["Data Collection"]["Tools Used"]
        opt.checkmark(node)
        node = main_node["Conclusion"]
        opt.checkmark(node)

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    def test2_checkmark_by_hash(_, corpus_testee3, local_testee32):
        opt, answer = local_testee32
        print(opt)

        main_node = corpus_testee3["Main Title"]
        node = main_node["Introduction"]
        opt.checkmark(hash(node))
        node = node["Background"]["Importance"]
        opt.checkmark(hash(node))
        node = main_node["Methods"]
        opt.checkmark(hash(node))
        node = node["Data Collection"]["Tools Used"]
        opt.checkmark(hash(node))
        node = main_node["Conclusion"]
        opt.checkmark(hash(node))

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )


# corpus w/ dynamic nodes  #####################################################
class TestDynamicNodes:

    # abbr  ====================================================================

    def test_checkmark_by_obj1(_, local_dynamic_testee1):
        bp = local_dynamic_testee1

        node = bp.corpus["Main Title"]["Introduction"]["Background"][
            "Importance"
        ]["Abbreviations"]

        assert bp.checkmark(node)
        assert bp.is_checkmarked(node)

    def test_checkmark_by_hash1(_, local_dynamic_testee1):
        bp = local_dynamic_testee1

        node = bp.corpus["Main Title"]["Introduction"]["Background"][
            "Importance"
        ]["Abbreviations"]
        node_hash = hash(node)

        assert bp.checkmark(node_hash)

        assert bp.is_checkmarked(node)

    def test_checkmark_by_name1(_, local_dynamic_testee1):
        bp = local_dynamic_testee1
        node = bp.corpus["Main Title"]["Introduction"]["Background"][
            "Importance"
        ]["Abbreviations"]
        ipt = "Abbreviations"

        assert bp.checkmark(ipt)

        assert bp.is_checkmarked(node)

    def test_checkmark_by_identifier1(_, local_dynamic_testee1):
        bp = local_dynamic_testee1
        node = bp.corpus["Main Title"]["Introduction"]["Background"][
            "Importance"
        ]["Abbreviations"]
        ipt = "{Abbreviations}"

        assert bp.checkmark(ipt)

        assert bp.is_checkmarked(node)

    # plc  =====================================================================

    def test_checkmark_by_obj2(_, local_dynamic_testee1):
        bp = local_dynamic_testee1

        node = bp.corpus["Main Title"]["Methods"]["Programming Languages Code"]

        assert bp.checkmark(node)
        assert bp.is_checkmarked(node)

    def test_checkmark_by_hash2(_, local_dynamic_testee1):
        bp = local_dynamic_testee1

        node = bp.corpus["Main Title"]["Methods"]["Programming Languages Code"]
        node_hash = hash(node)

        assert bp.checkmark(node_hash)

        assert bp.is_checkmarked(node)

    def test_checkmark_by_name2(_, local_dynamic_testee1):
        bp = local_dynamic_testee1

        node = bp.corpus["Main Title"]["Methods"]["Programming Languages Code"]
        ipt = "Programming Languages Code"

        assert bp.checkmark(ipt)

        assert bp.is_checkmarked(node)

    def test_checkmark_by_identifier2(_, local_dynamic_testee1):
        bp = local_dynamic_testee1
        node = bp.corpus["Main Title"]["Methods"]["Programming Languages Code"]
        ipt = "{Programming Languages Code}"

        bp.checkmark(ipt)

        assert bp.is_checkmarked(node)


# TODO TODO test for recursively
