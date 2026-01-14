"""
prompt_blueprint_parse_test.py

Unit Tests (using pytest) for: PromptBlueprint.parse()
"""

from kaye.gen_prompt import PromptCorpusNode, PromptBlueprint
from tests.gen_prompt import PROMPT1, PROMPT2

CORPUS1 = PromptCorpusNode.parse(PROMPT1)
CORPUS2 = PromptCorpusNode.parse(PROMPT2)

# test by data structure  ######################################################


class TestBasic1:  # use corpus1

    def test_full(_):
        corpus = CORPUS1
        bp_text = """    ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     └── License"""

        opt = PromptBlueprint.parse(corpus, bp_text, disable_prune=True)

        print(opt)
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 4
        assert opt.corpus is CORPUS1
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


# thorough tests by .generate_preview_tree()  ##################################
# i.e. dep on correct implementation of .generate_preview_tree()

# TODO thorough test after .generate_preview_tree

# BUG disable prune not working

# Bug tests for errors
