"""
prompt-bp-is_checkmarked_test.py

Unit Tests (using pytest) for: PromptBlueprint.is_enabled()
"""

# FIXME

from kaye.gen_prompt import PromptCorpusNode, PromptBlueprint
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


class XTest1:  # use corpus1  ###################################################

    def test_full(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]

        opt = bp.is_checkmarked(proj_node)
        print(repr(opt) + "\t" + repr(proj_node))
        assert opt

        # test Description
        _node = proj_node.children[0]
        print(repr(opt) + "\t" + repr(proj_node))
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # test Installation
        _node = proj_node.children[1]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # test License
        _node = proj_node.children[2]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

    def test_no_project(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_PARTIAL_1

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        opt = bp.is_checkmarked(proj_node)
        print(repr(opt) + "\t" + repr(proj_node))
        assert not opt

        # test Description
        _node = proj_node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # test Installation
        _node = proj_node.children[1]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # test License
        _node = proj_node.children[2]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

    def test_no_description(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_PARTIAL_2

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(bp)
        opt = len(bp) == 4

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        opt = bp.is_checkmarked(proj_node)
        print(repr(opt) + "\t" + repr(proj_node))
        assert opt

        # test Description
        _node = proj_node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # test Installation
        _node = proj_node.children[1]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # test License
        _node = proj_node.children[2]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert opt

    def test_empty(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_EMPTY

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(bp)
        opt = len(bp) == 4

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        opt = bp.is_checkmarked(proj_node)
        print(repr(opt) + "\t" + repr(proj_node))
        assert not opt

        # test Description
        _node = proj_node.children[0]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # test Installation
        _node = proj_node.children[1]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt

        # test License
        _node = proj_node.children[2]
        opt = bp.is_checkmarked(_node)
        print(repr(opt) + "\t" + repr(_node))
        assert not opt


class XTest3:  # use corpus3  ##############################################

    def test_full(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

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

    def test_part1(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_PARTIAL_1

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

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

    def test_part2(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_PARTIAL_2
        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

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

    def test_empty(_):
        corpus = CORPUS3

        bp_text = BLUEPRINT_3_EMPTY
        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

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


# err handling  ################################################################


def test_not_contained():  # a node that is not contained in bp at all
    pass  #  TODO
    # bp = PromptBlueprint.parse(CORPUS1, BLUEPRINT_1_FULL, disable_prune=True)
    # assert not bp.is_checkmarked(CORPUS3)
