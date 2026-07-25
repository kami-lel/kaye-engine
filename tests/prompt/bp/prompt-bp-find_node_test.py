"""
prompt-bp-find_node_test.py

Unit Tests (using pytest) for:


node_resolver.resolve_node()
"""

import pytest


from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode
from kaye_engine.prompt.blueprint.node_resolver import resolve_node


class Test1:  ##################################################################

    # Project Title  ===========================================================

    def test_by_name1(_, corpus_testee1, bp_testee2pa1):
        bp = bp_testee2pa1
        node = corpus_testee1["Project Title"]
        node_arg = "Project Title"

        node_obj, node_hash = resolve_node(bp.corpus, node_arg)

        assert node_obj.generate_lineage() == node.generate_lineage()
        assert node_hash == hash(node)

    def test_by_obj1(_, corpus_testee1, bp_testee2pa1):
        bp = bp_testee2pa1
        node = corpus_testee1["Project Title"]
        node_arg = node

        node_obj, node_hash = resolve_node(bp.corpus, node_arg)

        assert node_obj.generate_lineage() == node.generate_lineage()
        assert node_hash == hash(node)

    def test_by_hash1(_, corpus_testee1, bp_testee2pa1):
        bp = bp_testee2pa1
        node = corpus_testee1["Project Title"]
        node_arg = hash(node)

        node_obj, node_hash = resolve_node(bp.corpus, node_arg)

        assert node_obj.generate_lineage() == node.generate_lineage()
        assert node_hash == hash(node)

    # Description  =============================================================

    def test_by_name2(_, corpus_testee1, bp_testee2pa1):
        bp = bp_testee2pa1
        node = corpus_testee1["Project Title"]["Description"]
        node_arg = "Description"

        node_obj, node_hash = resolve_node(bp.corpus, node_arg)

        assert node_obj.generate_lineage() == node.generate_lineage()
        assert node_hash == hash(node)

    def test_by_obj3(_, corpus_testee1, bp_testee2pa1):
        bp = bp_testee2pa1
        node = corpus_testee1["Project Title"]["Description"]
        node_arg = node

        node_obj, node_hash = resolve_node(bp.corpus, node_arg)

        assert node_obj.generate_lineage() == node.generate_lineage()
        assert node_hash == hash(node)

    def test_by_hash2(_, corpus_testee1, bp_testee2pa1):
        bp = bp_testee2pa1
        node = corpus_testee1["Project Title"]["Description"]
        node_arg = hash(node)

        node_obj, node_hash = resolve_node(bp.corpus, node_arg)

        assert node_obj.generate_lineage() == node.generate_lineage()
        assert node_hash == hash(node)

    # err handling  ============================================================

    # bad typed  ***************************************************************

    def test_bad_type1(_, bp_testee2pa1):
        bp = bp_testee2pa1
        ipt = 12.5

        with pytest.raises(TypeError) as exec_info:
            resolve_node(bp.corpus, ipt)
        opt = exec_info.value.args[0]

        print(opt)

        assert opt == "must be BasePromptNode/int(hash value)/str(name): 12.5"

    def test_bad_type2(_, bp_testee2pa1):
        bp = bp_testee2pa1
        ipt = ["a", "b", "c"]

        with pytest.raises(TypeError) as exec_info:
            resolve_node(bp.corpus, ipt)
        opt = exec_info.value.args[0]

        print(opt)

        assert (
            opt
            == "must be "
            "BasePromptNode/int(hash value)/str(name): "
            "['a', 'b', 'c']"
        )

    # can't find  **************************************************************

    def test_miss_node_by_name1(_, bp_testee2pa1):
        bp = bp_testee2pa1
        ipt = "AAAZZZ"

        with pytest.raises(ValueError) as exec_info:
            resolve_node(bp.corpus, ipt)
        opt = exec_info.value.args[0]

        print(opt)

        assert opt == "no node in corpus with name: 'AAAZZZ'"

    def test_miss_node_by_hash1(_, bp_testee2pa1):
        bp = bp_testee2pa1
        ipt = hash(None)

        with pytest.raises(ValueError) as exec_info:
            resolve_node(bp.corpus, ipt)
        opt = exec_info.value.args[0]

        print(opt)

        assert opt == "no node in corpus with hash value: 4238894112"

    def test_miss_node_by_obj1(_, bp_testee2pa1):
        bp = bp_testee2pa1
        root = PromptCorpusNode("", None, [])
        ipt = PromptCorpusNode("AAAZZZ", root, [])

        with pytest.raises(ValueError) as exec_info:
            resolve_node(bp.corpus, ipt)
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "node not in corpus: PromptCorpusNode(AAAZZZ)"
