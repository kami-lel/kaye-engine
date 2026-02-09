"""
prompt-bp-parse-basic_test.py

Unit Tests (using pytest) for: PromptBlueprint.parse()
"""

# FIXME

from kaye.gen_prompt import PromptBlueprint

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


class XTestBasic1:  # use corpus1  ##############################################

    def test_full(_, test_corpus1):
        bp_text = BLUEPRINT_1_FULL

        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus1
        )

        print(opt)
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 4
        assert opt.corpus == test_corpus1
        assert opt.display_name == ""

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = test_corpus1.children[0]
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

    def test_no_project(_, test_corpus1):
        bp_text = BLUEPRINT_1_PARTIAL_1

        opt = PromptBlueprint.parse(bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 4

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = test_corpus1.children[0]
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

    def test_no_description(_, test_corpus1):
        bp_text = BLUEPRINT_1_PARTIAL_2

        opt = PromptBlueprint.parse(bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 4

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = test_corpus1.children[0]
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

    def test_empty(_, test_corpus1):
        bp_text = BLUEPRINT_1_EMPTY

        opt = PromptBlueprint.parse(bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 4

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = test_corpus1.children[0]
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


class XTestBasic3:  # use corpus3  ##############################################

    def test_full(_, test_corpus3):
        bp_text = BLUEPRINT_3_FULL

        opt = PromptBlueprint.parse(bp_text, disable_prune=True)

        print(opt)
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 10
        assert opt.corpus is test_corpus3
        assert opt.display_name == ""

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = test_corpus3.children[0]
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

    def test_part1(_, test_corpus3):
        bp_text = BLUEPRINT_3_PARTIAL_1

        opt = PromptBlueprint.parse(bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 10

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = test_corpus3.children[0]
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

    def test_part2(_, test_corpus3):
        bp_text = BLUEPRINT_3_PARTIAL_2
        opt = PromptBlueprint.parse(bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 10

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = test_corpus3.children[0]
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

    def test_empty(_, test_corpus3):
        bp_text = BLUEPRINT_3_EMPTY
        opt = PromptBlueprint.parse(bp_text, disable_prune=True)

        print(opt)
        assert len(opt) == 10

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = test_corpus3.children[0]
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
