"""
prompt_blueprint_contains_test.py

Unit Tests (using pytest) for: PromptBlueprint.__contains__()
"""

# BUG BUG BUG

from kaye.gen_prompt import PromptCorpusNode, PromptBlueprint
from tests.gen_prompt import PROMPT1, PROMPT3
from tests.gen_prompt.blueprint import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_1_EMPTY,
    BLUEPRINT_2_FULL,
    BLUEPRINT_2_PARTIAL_1,
    BLUEPRINT_2_PARTIAL_2,
    BLUEPRINT_2_EMPTY,
)

CORPUS1 = PromptCorpusNode.parse(PROMPT1)
CORPUS3 = PromptCorpusNode.parse(PROMPT3)


class Test1:  # use corpus1  ###################################################

    def test_full(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]

        opt = proj_node in bp
        print(opt + "\t" + repr(proj_node))
        assert opt

        # test Description
        _node = proj_node.children[0]
        print(opt + "\t" + repr(proj_node))
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # test Installation
        _node = proj_node.children[1]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # test License
        _node = proj_node.children[2]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

    def test_no_project(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_PARTIAL_1

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        opt = proj_node not in bp
        print(opt + "\t" + repr(proj_node))
        assert opt

        # test Description
        _node = proj_node.children[0]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # test Installation
        _node = proj_node.children[1]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # test License
        _node = proj_node.children[2]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
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
        opt = proj_node in bp
        print(opt + "\t" + repr(proj_node))
        assert opt

        # test Description
        _node = proj_node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # test Installation
        _node = proj_node.children[1]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # test License
        _node = proj_node.children[2]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
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
        opt = proj_node not in bp
        print(opt + "\t" + repr(proj_node))
        assert opt

        # test Description
        _node = proj_node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # test Installation
        _node = proj_node.children[1]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # test License
        _node = proj_node.children[2]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt


class Test3:  # use corpus3  ##############################################

    def test_full(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_2_FULL

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        opt = main_title_node in bp
        print(opt + "\t" + repr(main_title_node))
        assert opt

        # Introduction
        _node = main_title_node.children[0]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Background
        _node = _node.children[0]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Importance
        _node = _node.children[0]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Objective
        _node = _node.children[0]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Methods
        _node = main_title_node.children[1]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Data Collection
        _node = _node.children[0]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Tool Used
        _node = _node.children[0]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Future Work
        _node = _node.children[0]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Conclusion
        _node = main_title_node.children[2]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

    def test_part1(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_2_PARTIAL_1

        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        opt = main_title_node in bp
        print(opt + "\t" + repr(main_title_node))
        assert opt

        # Introduction
        _node = main_title_node.children[0]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Background
        _node = _node.children[0]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Importance
        _node = _node.children[0]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Objective
        _node = _node.children[0]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Methods
        _node = main_title_node.children[1]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Data Collection
        _node = _node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Tool Used
        _node = _node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Future Work
        _node = _node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Conclusion
        _node = main_title_node.children[2]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

    def test_part2(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_2_PARTIAL_2
        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(bp)
        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        opt = main_title_node in bp
        print(opt + "\t" + repr(main_title_node))
        assert opt

        # Introduction
        _node = main_title_node.children[0]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Background
        _node = _node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Importance
        _node = _node.children[0]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Objective
        _node = _node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Methods
        _node = main_title_node.children[1]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Data Collection
        _node = _node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Tool Used
        _node = _node.children[0]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Future Work
        _node = _node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Conclusion
        _node = main_title_node.children[2]
        opt = _node in bp
        print(opt + "\t" + repr(_node))
        assert opt

    def test_empty(_):
        corpus = CORPUS3

        bp_text = BLUEPRINT_2_EMPTY
        bp = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(bp)
        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        opt = main_title_node not in bp
        print(opt + "\t" + repr(main_title_node))
        assert opt

        # Introduction
        _node = main_title_node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Background
        _node = _node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Importance
        _node = _node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Objective
        _node = _node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Methods
        _node = main_title_node.children[1]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Data Collection
        _node = _node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Tool Used
        _node = _node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Future Work
        _node = _node.children[0]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt

        # Conclusion
        _node = main_title_node.children[2]
        opt = _node not in bp
        print(opt + "\t" + repr(_node))
        assert opt
