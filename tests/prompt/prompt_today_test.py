"""
prompt_today_test.py

Unit Tests (using pytest) for:

- TodayNote
"""

import re

from kaye.gen_prompt import PromptCorpusNode
from kaye.gen_prompt.today_node import TodayNode

from tests.prompt import PROMPT1

tree = PromptCorpusNode.parse(PROMPT1)


class TestToday:

    node = TodayNode(tree)

    def test_init(self):
        assert self.node.parent is tree
        assert self.node.name == "Today"
        assert self.node.id == "{Today}"

    def test_preview(self):
        opt = tree.generate_prompt_tree_preview(content_preview_lines=0)
        print(opt)
        assert opt == """○
├── Project Title
│   ├── Description
│   ├── Installation
│   └── License
└── Today"""

    def test_content_lines(self):
        lines = self.node.content_lines()
        assert re.fullmatch(r"Today: \d{4}-\d{2}-\d{2}", lines[0])
        assert re.fullmatch(r"Time: \d{2}:\d{2}:\d{2}", lines[1])
