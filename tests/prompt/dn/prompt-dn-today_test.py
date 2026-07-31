"""
prompt_today_test.py

Unit Tests (using pytest) for: TodayNote
"""

import re
import copy


import pytest


from kaye_engine.prompt.dynamic_nodes import TodayNode
from kaye_engine.prompt.prompt_corpus_node import HEADING_PREFIX_ELEMENT

TESTEE_TODAY_CONTENT = [
    "# (Today)",
    "**Current** Date and Time is:",
    "Date: ",
    "Time: ",
]


# pytest fixture  ##############################################################
@pytest.fixture(scope="session")
def local_corpus_testee1(corpus_testee1):
    return copy.deepcopy(corpus_testee1)


@pytest.fixture(scope="session")
def testee1(local_corpus_testee1):
    return TodayNode(local_corpus_testee1, preface=(TESTEE_TODAY_CONTENT[1],))


class TestToday:  ##############################################################

    def test_init(_, local_corpus_testee1, testee1):
        assert testee1.parent is local_corpus_testee1
        assert testee1.name == "(Today)"

    def test_preview(_, local_corpus_testee1):
        opt = local_corpus_testee1.generate_prompt_tree_preview(
            content_preview_lines=0
        )
        print(opt)
        assert opt == """○
├── Project Title
│   ├── Description
│   ├── Installation
│   └── License
└── (Today)"""

    def test_date(_, testee1):
        lines = testee1.content_lines()
        assert re.fullmatch(r"Date: \d{4}-\d{2}-\d{2}", lines[-2])

    def test_time(_, testee1):
        lines = testee1.content_lines()
        assert re.fullmatch(r"Time: \d{2}:\d{2}:\d{2}", lines[-1])

    @pytest.mark.parametrize("marker", TESTEE_TODAY_CONTENT)
    def test_today_content(_, testee1, marker):
        heading = HEADING_PREFIX_ELEMENT * testee1.depth + " " + testee1.name
        opt = heading + "\n" + "\n".join(testee1.content_lines())
        assert marker in opt


class TestCopy:  ###############################################################

    def test_copy1(_, testee1):
        copied = copy.copy(testee1)

        assert isinstance(copied, TodayNode)
        assert copied.name == "(Today)"
        assert copied.parent is None

    def test_deep_copy1(_, testee1):
        copied = copy.deepcopy(testee1)

        assert isinstance(copied, TodayNode)
        assert copied.name == "(Today)"
        assert copied.parent is None
