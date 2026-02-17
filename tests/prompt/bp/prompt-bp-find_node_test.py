"""
prompt-bp-find_node_test.py

Unit Tests (using pytest) for:


._checkmark_uncheckmark_is_checkmarked_find_node()
"""


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

    # TODO err handling


# TODO TODO
