"""
prompt_abbr_node_test.py

Unit Tests (using pytest) for:

- AbbrNode
"""

import pytest

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

    # test content_lines  ------------------------------------------------------

    def test_empty1(self):
        query = "some content without abbreviation"

        lines = self.node.content_lines(query=query)
        print(lines)
        assert lines == []

    def test_err1(self):

        with pytest.raises(ValueError) as exec_info:
            self.node.content_lines()

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "must provide kwarg: query"
