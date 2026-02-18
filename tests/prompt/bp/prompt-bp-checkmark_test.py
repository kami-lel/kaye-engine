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


# tests on prompt 1  ###########################################################
class Test11:  # ===============================================================

    # test .checkmark()  *******************************************************

    def test_checkmark_by_obj1(_, corpus_testee1, bp_testee1pa1):
        bp = bp_testee1pa1
        answer = BLUEPRINT_1_FULL

        print(repr(bp))
        node = corpus_testee1["Project Title"]

        bp.checkmark(node)

        print("#" * 80)
        print(repr(bp))

        assert (
            bp.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    def test_checkmark_by_hash1(_, corpus_testee1, bp_testee1pa1):
        bp = bp_testee1pa1
        answer = BLUEPRINT_1_FULL

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

    def test_checkmark_by_name1(_, corpus_testee1, bp_testee1pa1):
        bp = bp_testee1pa1
        answer = BLUEPRINT_1_FULL

        print(repr(bp))

        bp.checkmark("Project Title")

        print("#" * 80)
        print(repr(bp))

        assert (
            bp.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    # test +=  *****************************************************************

    def test_iadd_by_obj1(_, corpus_testee1, bp_testee1pa1):
        bp = bp_testee1pa1
        answer = BLUEPRINT_1_FULL

        print(repr(bp))
        node = corpus_testee1["Project Title"]

        bp += node

        print("#" * 80)
        print(repr(bp))

        assert (
            bp.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    def test_iadd_by_hash1(_, corpus_testee1, bp_testee1pa1):
        bp = bp_testee1pa1
        answer = BLUEPRINT_1_FULL

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

    def test_iadd_by_name1(_, bp_testee1pa1):
        bp = bp_testee1pa1
        answer = BLUEPRINT_1_FULL

        print(repr(bp))

        bp += "Project Title"

        print("#" * 80)
        print(repr(bp))

        assert (
            bp.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    # err handling  ************************************************************
    def test_bad_type1(_, bp_testee1pa1):
        bp = bp_testee1pa1
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

    def test_bad_type2(_, bp_testee1pa1):
        bp = bp_testee1pa1
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

    def test_bad_str_no_found1(_, bp_testee1pa1):
        bp = bp_testee1pa1
        ipt = "AAAZZZ"

        with pytest.raises(ValueError) as exec_info:
            bp.checkmark(ipt)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "no node in corpus with name/identifier: 'AAAZZZ'"

    def test_bad_hash(self, bp_testee1pa1):
        opt = bp_testee1pa1

        with pytest.raises(ValueError) as exec_info:
            opt.checkmark(5)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "no node in corpus with hash value: 5"

    def test_bad_obj(self, bp_testee1pa1, corpus_testee3):
        opt = bp_testee1pa1
        bad_node = corpus_testee3.children[0]

        with pytest.raises(ValueError) as exec_info:
            opt.checkmark(bad_node)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "node not in corpus: PromptCorpusNode(Main Title)"


class Test12:  # ===============================================================

    def test2_checkmark_by_obj(_, bp_testee1pa2, corpus_testee1):
        opt = bp_testee1pa2
        answer = BLUEPRINT_1_FULL

        print(opt)

        node = corpus_testee1["Project Title"]["Description"]
        opt.checkmark(node)

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    def test2_checkmark_by_hash(_, bp_testee1pa2, corpus_testee1):
        opt = bp_testee1pa2
        answer = BLUEPRINT_1_FULL

        print(opt)

        node = corpus_testee1["Project Title"]["Description"]
        node_hash = hash(node)
        opt.checkmark(node_hash)

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )


class Test2:  # tests on prompt 2  ############################################
    def test1_checkmark_by_obj(_, corpus_testee2, bp_testee2pa1):
        opt = bp_testee2pa1
        answer = BLUEPRINT_2_FULL
        print(opt)

        proj_node = corpus_testee2["Project Title"]
        opt.checkmark(proj_node["Description"]).checkmark(
            proj_node["Usage"]
        ).checkmark(proj_node["License"])

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )

    def test1_checkmark_by_hash(_, corpus_testee2, bp_testee2pa1):
        opt = bp_testee2pa1
        answer = BLUEPRINT_2_FULL
        print(opt)

        proj_node = corpus_testee2["Project Title"]
        for h in [
            hash(proj_node[name])
            for name in ("Description", "Usage", "License")
        ]:
            opt.checkmark(h)

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == answer
        )


# tests on prompt 3  ###########################################################
class Test31:  # ===============================================================

    def test1_checkmark_by_obj(_, corpus_testee3, bp_testee3pa1):
        opt = bp_testee3pa1
        answer = BLUEPRINT_3_FULL

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

    def test1_checkmark_by_hash(_, corpus_testee3, bp_testee3pa1):
        opt = bp_testee3pa1
        answer = BLUEPRINT_3_FULL

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

    def test2_checkmark_by_obj(_, corpus_testee3, bp_testee3pa2):
        opt = bp_testee3pa2
        answer = BLUEPRINT_3_FULL

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

    def test2_checkmark_by_hash(_, corpus_testee3, bp_testee3pa2):
        opt = bp_testee3pa2
        answer = BLUEPRINT_3_FULL
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

    def test_checkmark_by_obj1(_, dynamic_bp_testee1):
        bp = copy.deepcopy(dynamic_bp_testee1)

        node = dynamic_bp_testee1.corpus["Main Title"]["Introduction"][
            "Background"
        ]["Importance"]["Abbreviations"]

        assert bp.checkmark(node)
        assert bp.is_checkmarked(node)

    def test_checkmark_by_hash1(_, dynamic_bp_testee1):
        bp = copy.deepcopy(dynamic_bp_testee1)

        node = dynamic_bp_testee1.corpus["Main Title"]["Introduction"][
            "Background"
        ]["Importance"]["Abbreviations"]
        node_hash = hash(node)

        assert bp.checkmark(node_hash)

        assert bp.is_checkmarked(node)

    def test_checkmark_by_name1(_, dynamic_bp_testee1):
        bp = copy.deepcopy(dynamic_bp_testee1)
        node = dynamic_bp_testee1.corpus["Main Title"]["Introduction"][
            "Background"
        ]["Importance"]["Abbreviations"]
        ipt = "Abbreviations"

        assert bp.checkmark(ipt)

        assert bp.is_checkmarked(node)

    def test_checkmark_by_identifier1(_, dynamic_bp_testee1):
        bp = copy.deepcopy(dynamic_bp_testee1)
        node = dynamic_bp_testee1.corpus["Main Title"]["Introduction"][
            "Background"
        ]["Importance"]["Abbreviations"]
        ipt = "{Abbreviations}"

        assert bp.checkmark(ipt)

        assert bp.is_checkmarked(node)

    # plc  =====================================================================

    def test_checkmark_by_obj2(_, dynamic_bp_testee1):
        bp = copy.deepcopy(dynamic_bp_testee1)

        node = dynamic_bp_testee1.corpus["Main Title"]["Methods"][
            "Programming Languages Code"
        ]

        assert bp.checkmark(node)
        assert bp.is_checkmarked(node)

    def test_checkmark_by_hash2(_, dynamic_bp_testee1):
        bp = copy.deepcopy(dynamic_bp_testee1)

        node = dynamic_bp_testee1.corpus["Main Title"]["Methods"][
            "Programming Languages Code"
        ]
        node_hash = hash(node)

        assert bp.checkmark(node_hash)

        assert bp.is_checkmarked(node)

    def test_checkmark_by_name2(_, dynamic_bp_testee1):
        bp = copy.deepcopy(dynamic_bp_testee1)

        node = dynamic_bp_testee1.corpus["Main Title"]["Methods"][
            "Programming Languages Code"
        ]
        ipt = "Programming Languages Code"

        assert bp.checkmark(ipt)

        assert bp.is_checkmarked(node)

    def test_checkmark_by_identifier2(_, dynamic_bp_testee1):
        bp = copy.deepcopy(dynamic_bp_testee1)
        node = dynamic_bp_testee1.corpus["Main Title"]["Methods"][
            "Programming Languages Code"
        ]
        ipt = "{Programming Languages Code}"

        bp.checkmark(ipt)

        assert bp.is_checkmarked(node)
