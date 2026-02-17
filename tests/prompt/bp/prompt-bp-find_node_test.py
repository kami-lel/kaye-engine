"""
prompt-bp-find_node_test.py

Unit Tests (using pytest) for:


._checkmark_uncheckmark_is_checkmarked_find_node()
"""

import pytest


class Test1:  ##################################################################

    # Project Title  ===========================================================

    def test_by_name1(_, corpus_testee1, checkmark_bp_testee11):
        bp = checkmark_bp_testee11
        node = corpus_testee1["Project Title"]
        node_arg = "Project Title"

        node_obj, node_hash = (
            bp._checkmark_uncheckmark_is_checkmarked_find_node(node_arg)
        )

        assert (
            node_obj.generate_identifier_lineage()
            == node.generate_identifier_lineage()
        )
        assert node_hash == hash(node)

    def test_by_obj1(_, corpus_testee1, checkmark_bp_testee11):
        bp = checkmark_bp_testee11
        node = corpus_testee1["Project Title"]
        node_arg = node

        node_obj, node_hash = (
            bp._checkmark_uncheckmark_is_checkmarked_find_node(node_arg)
        )

        assert (
            node_obj.generate_identifier_lineage()
            == node.generate_identifier_lineage()
        )
        assert node_hash == hash(node)

    def test_by_hash1(_, corpus_testee1, checkmark_bp_testee11):
        bp = checkmark_bp_testee11
        node = corpus_testee1["Project Title"]
        node_arg = hash(node)

        node_obj, node_hash = (
            bp._checkmark_uncheckmark_is_checkmarked_find_node(node_arg)
        )

        assert (
            node_obj.generate_identifier_lineage()
            == node.generate_identifier_lineage()
        )
        assert node_hash == hash(node)

    # err handling  ============================================================

    # bad typed  ***************************************************************

    def test_bad_type1(_, checkmark_bp_testee11):
        bp = checkmark_bp_testee11
        ipt = 12.5

        with pytest.raises(TypeError) as exec_info:
            bp.checkmark(ipt)
        opt = exec_info.value.args[0]

        print(opt)

        assert (
            opt
            == "must be "
            "BasePromptNode/int(hash value)/str(name/identifier): "
            "12.5"
        )

    def test_bad_type2(_, checkmark_bp_testee11):
        bp = checkmark_bp_testee11
        ipt = ["a", "b", "c"]

        with pytest.raises(TypeError) as exec_info:
            bp.checkmark(ipt)
        opt = exec_info.value.args[0]

        print(opt)

        assert (
            opt
            == "must be "
            "BasePromptNode/int(hash value)/str(name/identifier): "
            "['a', 'b', 'c']"
        )

    # can't find  **************************************************************

    def test_miss_node_by_name1(_, checkmark_bp_testee11):
        bp = checkmark_bp_testee11
        ipt = "AAAZZZ"

        with pytest.raises(ValueError) as exec_info:
            bp.checkmark(ipt)
        opt = exec_info.value.args[0]

        print(opt)

        assert (
            opt == "no node with name/identifier/hash value in corpus: 'AAAZZZ'"
        )

    def test_miss_node_by_hash1(_, checkmark_bp_testee11):
        bp = checkmark_bp_testee11
        ipt = hash(None)

        with pytest.raises(ValueError) as exec_info:
            bp.checkmark(ipt)
        opt = exec_info.value.args[0]

        print(opt)

        assert (
            opt
            == "no node with name/identifier/hash value in corpus: 4238894112"
        )
