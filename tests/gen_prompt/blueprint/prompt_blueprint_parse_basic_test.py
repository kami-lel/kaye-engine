"""
prompt_blueprint_parse_basic_test.py

Unit Tests (using pytest) for: PromptBlueprint.parse()

this perform basic test of the parsed blueprint
"""

from kaye.gen_prompt import PromptCorpusNode, PromptBlueprint
from tests.gen_prompt import PROMPT1, PROMPT3
from tests.gen_prompt.blueprint import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_1_EMPTY,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_2,
    BLUEPRINT_3_EMPTY,
)

CORPUS1 = PromptCorpusNode.parse(PROMPT1)
CORPUS3 = PromptCorpusNode.parse(PROMPT3)


class TestBasic1:  # use corpus1  ##############################################

    def test_full(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_FULL

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 4
        assert opt.corpus is corpus
        assert opt.display_name == ""

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        _hash = hash(proj_node)
        assert _hash in opt
        assert opt[_hash]

        # test Description
        _node = proj_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # test Installation
        _node = proj_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # test License
        _node = proj_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

    def test_no_project(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_PARTIAL_1

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 4

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        _hash = hash(proj_node)
        assert _hash in opt
        assert not opt[_hash]

        # test Description
        _node = proj_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # test Installation
        _node = proj_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # test License
        _node = proj_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

    def test_no_description(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_PARTIAL_2

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 4

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        _hash = hash(proj_node)
        assert _hash in opt
        assert opt[_hash]

        # test Description
        _node = proj_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # test Installation
        _node = proj_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # test License
        _node = proj_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

    def test_empty(_):
        corpus = CORPUS1
        bp_text = BLUEPRINT_1_EMPTY

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 4

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus.children[0]
        _hash = hash(proj_node)
        assert _hash in opt
        assert not opt[_hash]

        # test Description
        _node = proj_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # test Installation
        _node = proj_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # test License
        _node = proj_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]


class TestBasic3:  # use corpus3  ##############################################

    def test_full(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_FULL

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 10
        assert opt.corpus is corpus
        assert opt.display_name == ""

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        _hash = hash(main_title_node)
        assert _hash in opt
        assert opt[_hash]

        # Introduction
        _node = main_title_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Background
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Importance
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Objective
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Methods
        _node = main_title_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Data Collection
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Tool Used
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Future Work
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Conclusion
        _node = main_title_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

    def test_part1(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_PARTIAL_1

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 10

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        _hash = hash(main_title_node)
        assert _hash in opt
        assert opt[_hash]

        # Introduction
        _node = main_title_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Background
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Importance
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Objective
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Methods
        _node = main_title_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Data Collection
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Tool Used
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Future Work
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Conclusion
        _node = main_title_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

    def test_part2(_):
        corpus = CORPUS3
        bp_text = BLUEPRINT_3_PARTIAL_2
        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 10

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        _hash = hash(main_title_node)
        assert _hash in opt
        assert opt[_hash]

        # Introduction
        _node = main_title_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Background
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Importance
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Objective
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Methods
        _node = main_title_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Data Collection
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Tool Used
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Future Work
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert opt[_hash]

        # Conclusion
        _node = main_title_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

    def test_empty(_):
        corpus = CORPUS3

        bp_text = BLUEPRINT_3_EMPTY
        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 10

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus.children[0]
        _hash = hash(main_title_node)
        assert _hash in opt
        assert not opt[_hash]

        # Introduction
        _node = main_title_node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Background
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Importance
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Objective
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Methods
        _node = main_title_node.children[1]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Data Collection
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Tool Used
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Future Work
        _node = _node.children[0]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]

        # Conclusion
        _node = main_title_node.children[2]
        _hash = hash(_node)
        assert _hash in opt
        assert not opt[_hash]


# setting display_name  ########################################################


class TestDisplayName:

    def test_dft(_):
        bp_text = BLUEPRINT_1_FULL

        opt = PromptBlueprint.parse(CORPUS1, bp_text)

        print(opt)
        assert opt.display_name == ""

    def test1(_):
        bp_text = BLUEPRINT_1_FULL
        display_name = "My Blueprint"

        opt = PromptBlueprint.parse(
            CORPUS1, bp_text, display_name=display_name
        )

        print(opt)
        assert opt.display_name == display_name

    def test2(_):
        bp_text = BLUEPRINT_1_PARTIAL_1
        display_name = "My Blueprint"

        opt = PromptBlueprint.parse(
            CORPUS1, bp_text, display_name=display_name
        )

        print(opt)
        assert opt.display_name == display_name

    def test3(_):
        bp_text = BLUEPRINT_3_EMPTY
        display_name = "My Blueprint"

        opt = PromptBlueprint.parse(
            CORPUS3, bp_text, display_name=display_name
        )

        print(opt)
        assert opt.display_name == display_name


# Bug tests for errors
