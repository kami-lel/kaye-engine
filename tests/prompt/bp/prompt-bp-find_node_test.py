"""
prompt-bp-find_node_test.py

Unit Tests (using pytest) for:


._find_node_in_corpus_and_blueprint()
"""

import pytest


class Test1:  ##################################################################

    # Project Title  ===========================================================

    def test_by_name1(_, corpus_testee1, bp_testee1pa1):
        bp = bp_testee1pa1
        node = corpus_testee1["Project Title"]
        node_arg = "Project Title"

        node_obj, node_hash, is_contained = (
            bp._find_node_in_corpus_and_blueprint(node_arg)
        )

        assert (
            node_obj.generate_identifier_lineage()
            == node.generate_identifier_lineage()
        )
        assert node_hash == hash(node)
        assert is_contained

    def test_by_obj1(_, corpus_testee1, bp_testee1pa1):
        bp = bp_testee1pa1
        node = corpus_testee1["Project Title"]
        node_arg = node

        node_obj, node_hash, is_contained = (
            bp._find_node_in_corpus_and_blueprint(node_arg)
        )

        assert (
            node_obj.generate_identifier_lineage()
            == node.generate_identifier_lineage()
        )
        assert node_hash == hash(node)
        assert is_contained

    def test_by_hash1(_, corpus_testee1, bp_testee1pa1):
        bp = bp_testee1pa1
        node = corpus_testee1["Project Title"]
        node_arg = hash(node)

        node_obj, node_hash, is_contained = (
            bp._find_node_in_corpus_and_blueprint(node_arg)
        )

        assert (
            node_obj.generate_identifier_lineage()
            == node.generate_identifier_lineage()
        )
        assert node_hash == hash(node)
        assert is_contained

    # Description  =============================================================

    def test_by_name2(_, corpus_testee1, bp_testee1pa1):
        bp = bp_testee1pa1
        node = corpus_testee1["Project Title"]["Description"]
        node_arg = "Description"

        node_obj, node_hash, is_contained = (
            bp._find_node_in_corpus_and_blueprint(node_arg)
        )

        assert (
            node_obj.generate_identifier_lineage()
            == node.generate_identifier_lineage()
        )
        assert node_hash == hash(node)
        assert is_contained

    def test_by_obj3(_, corpus_testee1, bp_testee1pa1):
        bp = bp_testee1pa1
        node = corpus_testee1["Project Title"]["Description"]
        node_arg = node

        node_obj, node_hash, is_contained = (
            bp._find_node_in_corpus_and_blueprint(node_arg)
        )

        assert (
            node_obj.generate_identifier_lineage()
            == node.generate_identifier_lineage()
        )
        assert node_hash == hash(node)
        assert is_contained

    def test_by_hash2(_, corpus_testee1, bp_testee1pa1):
        bp = bp_testee1pa1
        node = corpus_testee1["Project Title"]["Description"]
        node_arg = hash(node)

        node_obj, node_hash, is_contained = (
            bp._find_node_in_corpus_and_blueprint(node_arg)
        )

        assert (
            node_obj.generate_identifier_lineage()
            == node.generate_identifier_lineage()
        )
        assert node_hash == hash(node)
        assert is_contained

    # err handling  ============================================================

    # bad typed  ***************************************************************

    def test_bad_type1(_, bp_testee1pa1):
        bp = bp_testee1pa1
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

    def test_bad_type2(_, bp_testee1pa1):
        bp = bp_testee1pa1
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

    def test_miss_node_by_name1(_, bp_testee1pa1):
        bp = bp_testee1pa1
        ipt = "AAAZZZ"

        with pytest.raises(ValueError) as exec_info:
            bp.checkmark(ipt)
        opt = exec_info.value.args[0]

        print(opt)

        assert (
            opt == "no node in corpus with name/identifier/hash value: 'AAAZZZ'"
        )

    def test_miss_node_by_hash1(_, bp_testee1pa1):
        bp = bp_testee1pa1
        ipt = hash(None)

        with pytest.raises(ValueError) as exec_info:
            bp.checkmark(ipt)
        opt = exec_info.value.args[0]

        print(opt)

        assert (
            opt
            == "no node in corpus with name/identifier/hash value: 4238894112"
        )
