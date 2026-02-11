"""
prompt_today_test.py

Unit Tests (using pytest) for: TodayNote
"""

import re
import copy


import pytest


from kaye.gen_prompt.today_node import TodayNode


@pytest.fixture
def testee1(test_corpus1):
    return TodayNode(test_corpus1)


class TestToday:  ##############################################################

    def test_init(_, test_corpus1, testee1):
        assert testee1.parent is test_corpus1
        assert testee1.name == "Today"
        assert testee1.id == "{Today}"

    def test_preview(_, test_corpus1, testee1):
        opt = test_corpus1.generate_prompt_tree_preview(content_preview_lines=0)
        print(opt)
        assert opt == """○
├── Project Title
│   ├── Description
│   ├── Installation
│   └── License
└── Today"""

    def test_content_lines(_, test_corpus1, testee1):
        testee1 = TodayNode(test_corpus1)
        lines = testee1.content_lines()
        assert re.fullmatch(r"Today: \d{4}-\d{2}-\d{2}", lines[0])
        assert re.fullmatch(r"Time: \d{2}:\d{2}:\d{2}", lines[1])


class TestCopy:  ###############################################################

    def test_copy1(_, test_corpus1, testee1):
        copied = copy.copy(testee1)

        assert isinstance(copied, TodayNode)
        assert copied.name == "Today"
        assert copied.parent is test_corpus1

    def test_deep_copy1(_, test_corpus1, testee1):
        copied = copy.deepcopy(testee1)

        assert isinstance(copied, TodayNode)
        assert copied.name == "Today"
        assert copied.parent is test_corpus1
