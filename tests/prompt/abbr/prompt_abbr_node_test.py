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

        # TODO TODO more tests

        # "For example, when I think about doing -g tasks, I realize that it signifies continuous effort, which might sometimes be more important than the actual result. The choice of /* in many contexts means either one thing or another, and sometimes it can be difficult to determine which option is better, especially when both seem to have merits."

        # "Furthermore, the symbol = is used to express that two things are equal or equivalent, which can be crucial in mathematical or logical discussions, but often in life, things are not so straightforward, and we must consider multiple factors."

        # "In addition, I want to mention that the emoji 💡 represents information or informational content, which is vital when trying to understand complex ideas or concepts. When I prepare notes 4 you, Sir, I try to include all relevant details about the topic abt to ensure clarity. Sometimes I wonder if I can provide a/t everything you need, Sir, or if I should focus on specific points. I also realize that I Cx provide assistance only within my limits, Sir, and I must be careful not to overstep. Lastly, I take note that o. can be used as a prefix to indicate over- or excess, and I always try to be precise with the xsi that exist in any given situation, Sir."

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
