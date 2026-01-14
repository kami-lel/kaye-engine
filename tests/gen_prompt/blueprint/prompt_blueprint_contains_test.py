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

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        assert proj_node in opt

        # test Description
        _node = proj_node.children[0]
        assert _node in opt

        # test Installation
        _node = proj_node.children[1]
        assert _node in opt

        # test License
        _node = proj_node.children[2]
        assert _node in opt

    def test_no_project(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_PARTIAL_1

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        assert proj_node not in opt

        # test Description
        _node = proj_node.children[0]
        assert _node in opt

        # test Installation
        _node = proj_node.children[1]
        assert _node in opt

        # test License
        _node = proj_node.children[2]
        assert _node in opt

    def test_no_description(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_PARTIAL_2

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 4

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        assert proj_node in opt

        # test Description
        _node = proj_node.children[0]
        assert _node not in opt

        # test Installation
        _node = proj_node.children[1]
        assert _node in opt

        # test License
        _node = proj_node.children[2]
        assert _node in opt

    def test_empty(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_EMPTY

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 4

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        assert proj_node not in opt

        # test Description
        _node = proj_node.children[0]
        assert _node not in opt

        # test Installation
        _node = proj_node.children[1]
        assert _node not in opt

        # test License
        _node = proj_node.children[2]
        assert _node not in opt


class Test3:  # use corpus3  ##############################################

    def test_full(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_2_FULL

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        assert main_title_node in opt

        # Introduction
        _node = main_title_node.children[0]
        assert _node in opt

        # Background
        _node = _node.children[0]
        assert _node in opt

        # Importance
        _node = _node.children[0]
        assert _node in opt

        # Objective
        _node = _node.children[0]
        assert _node in opt

        # Methods
        _node = main_title_node.children[1]
        assert _node in opt

        # Data Collection
        _node = _node.children[0]
        assert _node in opt

        # Tool Used
        _node = _node.children[0]
        assert _node in opt

        # Future Work
        _node = _node.children[0]
        assert _node in opt

        # Conclusion
        _node = main_title_node.children[2]
        assert _node in opt

    def test_part1(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_2_PARTIAL_1

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        assert main_title_node in opt

        # Introduction
        _node = main_title_node.children[0]
        assert _node in opt

        # Background
        _node = _node.children[0]
        assert _node in opt

        # Importance
        _node = _node.children[0]
        assert _node in opt

        # Objective
        _node = _node.children[0]
        assert _node in opt

        # Methods
        _node = main_title_node.children[1]
        assert _node not in opt

        # Data Collection
        _node = _node.children[0]
        assert _node not in opt

        # Tool Used
        _node = _node.children[0]
        assert _node not in opt

        # Future Work
        _node = _node.children[0]
        assert _node not in opt

        # Conclusion
        _node = main_title_node.children[2]
        assert _node in opt

    def test_part2(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_2_PARTIAL_2
        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        assert main_title_node in opt

        # Introduction
        _node = main_title_node.children[0]
        assert _node in opt

        # Background
        _node = _node.children[0]
        assert _node not in opt

        # Importance
        _node = _node.children[0]
        assert _node in opt

        # Objective
        _node = _node.children[0]
        assert _node not in opt

        # Methods
        _node = main_title_node.children[1]
        assert _node in opt

        # Data Collection
        _node = _node.children[0]
        assert _node not in opt

        # Tool Used
        _node = _node.children[0]
        assert _node in opt

        # Future Work
        _node = _node.children[0]
        assert _node not in opt

        # Conclusion
        _node = main_title_node.children[2]
        assert _node in opt

    def test_empty(_):
        corpus = CORPUS3

        bp_text = BLUEPRINT_2_EMPTY
        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        assert main_title_node not in opt

        # Introduction
        _node = main_title_node.children[0]
        assert _node not in opt

        # Background
        _node = _node.children[0]
        assert _node not in opt

        # Importance
        _node = _node.children[0]
        assert _node not in opt

        # Objective
        _node = _node.children[0]
        assert _node not in opt

        # Methods
        _node = main_title_node.children[1]
        assert _node not in opt

        # Data Collection
        _node = _node.children[0]
        assert _node not in opt

        # Tool Used
        _node = _node.children[0]
        assert _node not in opt

        # Future Work
        _node = _node.children[0]
        assert _node not in opt

        # Conclusion
        _node = main_title_node.children[2]
        assert _node not in opt
