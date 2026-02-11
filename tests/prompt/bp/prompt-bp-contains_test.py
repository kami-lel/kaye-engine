"""
prompt-bp-contains_test.py

Unit Tests (using pytest) for: PromptBlueprint.__contains__()
"""

from kaye.gen_prompt.prompt_blueprint import PromptBlueprint
from tests.prompt.bp import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_3_FULL,
)


class Test1:  # use corpus1  ###################################################

    def test_full(_, corpus_testee1):
        bp_text = BLUEPRINT_1_FULL

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee1
        )

        # test entries  --------------------------------------------------------
        # test Project Title
        proj_node = corpus_testee1.children[0]

        opt = proj_node in bp
        print(repr(opt) + "\t" + repr(proj_node))
        assert opt

        # test Description
        _node = proj_node.children[0]
        print(repr(opt) + "\t" + repr(proj_node))
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # test Installation
        _node = proj_node.children[1]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # test License
        _node = proj_node.children[2]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt


class Test3:  # use corpus3  ##############################################

    def test_full(_, corpus_testee3):
        bp_text = BLUEPRINT_3_FULL

        bp = PromptBlueprint.parse(
            bp_text,
            disable_prune=True,
            corpus_override=corpus_testee3,
        )

        # test entries  --------------------------------------------------------
        # Main Title
        main_title_node = corpus_testee3.children[0]
        opt = main_title_node in bp
        print(repr(opt) + "\t" + repr(main_title_node))
        assert opt

        # Introduction
        _node = main_title_node.children[0]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Background
        _node = _node.children[0]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Importance
        _node = _node.children[0]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Objective
        _node = _node.children[0]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Methods
        _node = main_title_node.children[1]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Data Collection
        _node = _node.children[0]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Tool Used
        _node = _node.children[0]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Future Work
        _node = _node.children[0]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt

        # Conclusion
        _node = main_title_node.children[2]
        opt = _node in bp
        print(repr(opt) + "\t" + repr(_node))
        assert opt
