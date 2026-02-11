"""
prompt_today_test.py

Unit Tests (using pytest) for:

- TodayNote
"""

import re

from kaye.gen_prompt import PromptCorpusNode
from kaye.gen_prompt.today_node import TodayNode


class TestToday:
    # BUG

    def test_init(_, test_corpus1):
        node = TodayNode(test_corpus1)
        assert node.parent is test_corpus1
        assert node.name == "Today"
        assert node.id == "{Today}"

    def test_preview(_, test_corpus1):
        opt = test_corpus1.generate_prompt_tree_preview(content_preview_lines=0)
        print(opt)
        assert opt == """○
├── Project Title
│   ├── Description
│   ├── Installation
│   └── License
└── Today"""

    def test_content_lines(_, test_corpus1):
        node = TodayNode(test_corpus1)
        lines = node.content_lines()
        assert re.fullmatch(r"Today: \d{4}-\d{2}-\d{2}", lines[0])
        assert re.fullmatch(r"Time: \d{2}:\d{2}:\d{2}", lines[1])
