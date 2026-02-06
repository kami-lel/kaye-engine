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


class TestAbbrNode:

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

    def test_fx1(self):
        query = "I am try.g to op.g on menu."

        lines = self.node.content_lines(query=query)

        print(lines)
        assert set(lines) == {"- op:operate,operation,operator", "- .g:-ing"}

    def test_fx2(self):
        query = (
            "The ind rev catalyzed a tectonic shift fr artisanal produc.n to"
            " mechanized manufacture, precipitating urbanization, the rise of"
            " factory labor, and new cls dynamics; & innovations in pub health,"
            " and pol repr. The period's cul ramifications incl the spread of"
            " literacy and reorder modn soc."
        )

        lines = self.node.content_lines(query=query)

        print(lines)

        # BUG BUG
        assert set(lines) == {
            "- modn:modern,modernization",
            "- &:and",
            "- pol:politic,politics,political",
            "- repr:representation",
            "- soc:society",
            "- cul:culture,cultural",
            "- rev:revolution",
            "- fr:from",
            "- cls:class,classic,classicism,classify,classical",
            "- pub:public;publish",
            "- ind:industry,industrial",
        }

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
