"""
prompt-lc_test.py

Unit Tests (using pytest) for:

LanguageCodeNode
"""

import copy


import pytest


from kaye.prompt.abbr_nodes import LanguageCodeNode


# pytest fixtures  #############################################################
@pytest.fixture(scope="session")
def local_corpus_testee1(corpus_testee1):
    return copy.deepcopy(corpus_testee1)


@pytest.fixture(scope="session")
def testee1(local_corpus_testee1):
    return LanguageCodeNode(local_corpus_testee1)


# pytest  ######################################################################


class TestInit:  # =============================================================

    def test1(_, testee1, local_corpus_testee1):
        assert testee1.parent is local_corpus_testee1
        assert testee1.name == "{Languages Code}"

    def test_preview1(_, local_corpus_testee1):
        opt = local_corpus_testee1.generate_prompt_tree_preview(
            content_preview_lines=0
        )
        print(opt)
        assert opt == """○
├── Project Title
│   ├── Description
│   ├── Installation
│   └── License
└── {Languages Code}"""


class TestCopy:  # =============================================================

    def test_copy1(_, testee1):
        copied = copy.copy(testee1)

        assert isinstance(copied, LanguageCodeNode)
        assert copied.name == "{Languages Code}"
        assert copied.parent is None

    def test_deep_copy1(_, testee1):
        copied = copy.deepcopy(testee1)

        assert isinstance(copied, LanguageCodeNode)
        assert copied.name == "{Languages Code}"
        assert copied.parent is None


class TestContentLines:  # =====================================================

    def test1(_, testee1):
        opt = testee1.content_lines()
        print(opt)
        assert opt == [
            "-`de`:Deutsch",
            "-`en`:English",
            "-`zh`:中文",
            "-`zhs`:大陆简体中文",
            "-`zht`:香港繁體中文",
        ]
