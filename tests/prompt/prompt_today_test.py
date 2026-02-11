"""
prompt_today_test.py

Unit Tests (using pytest) for: TodayNote
"""

import re
import copy


import pytest


from kaye.gen_prompt.today_node import TodayNode


@pytest.fixture
def testee1(corpus_testee1):
    return TodayNode(corpus_testee1)


class TestToday:  ##############################################################

    def test_init(_, corpus_testee1, testee1):
        assert testee1.parent is corpus_testee1
        assert testee1.name == "Today"
        assert testee1.id == "{Today}"

    def test_preview(_, corpus_testee1, testee1):
        opt = corpus_testee1.generate_prompt_tree_preview(
            content_preview_lines=0
        )
        print(opt)
        assert opt == """○
├── Project Title
│   ├── Description
│   ├── Installation
│   └── License
└── Today"""

    def test_content_lines(_, corpus_testee1, testee1):
        testee1 = TodayNode(corpus_testee1)
        lines = testee1.content_lines()
        assert re.fullmatch(r"Today: \d{4}-\d{2}-\d{2}", lines[0])
        assert re.fullmatch(r"Time: \d{2}:\d{2}:\d{2}", lines[1])


class TestCopy:  ###############################################################

    def test_copy1(_, corpus_testee1, testee1):
        copied = copy.copy(testee1)

        assert isinstance(copied, TodayNode)
        assert copied.name == "Today"
        assert copied.parent is corpus_testee1

    def test_deep_copy1(_, corpus_testee1, testee1):
        copied = copy.deepcopy(testee1)

        assert isinstance(copied, TodayNode)
        assert copied.name == "Today"
        assert copied.parent is corpus_testee1
