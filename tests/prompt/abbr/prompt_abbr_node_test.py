"""
prompt_abbr_node_test.py

Unit Tests (using pytest) for:

- AbbrNode
"""

from kaye.gen_prompt import PromptCorpusNode
from kaye.gen_prompt.abbr_nodes import AbbrNode


from tests.prompt import PROMPT1

tree = PromptCorpusNode.parse(PROMPT1)


class TestPLC:

    node = AbbrNode(tree)

    def test_init(self):
        self.node.parent is tree
        self.node.name == "Abbreviations"
        self.node.id == "{Abbreviations}"

    def test_preview(self):
        opt = tree.generate_prompt_tree_preview(content_preview_lines=0)
        print(opt)
        assert opt == """○
├── Project Title
│   ├── Description
│   ├── Installation
│   └── License
└── Abbreviations"""

    # test query function  -----------------------------------------------------

    # TODO TODO
