"""
prompt-dn-u3d_test.py

Unit Tests (using pytest) for:

UnityEngineAbbrNode
"""

import copy


import pytest


from kaye.prompt.abbr_nodes import UnityEngineAbbrNode


# pytest fixtures  #############################################################
@pytest.fixture(scope="session")
def local_corpus_testee1(corpus_testee1):
    return copy.deepcopy(corpus_testee1)


@pytest.fixture(scope="session")
def testee1(local_corpus_testee1):
    return UnityEngineAbbrNode(local_corpus_testee1)


class TestInit:  ###############################################################

    def test1(_, testee1, local_corpus_testee1):
        assert testee1.parent is local_corpus_testee1
        assert testee1.name == "{Unity Engine Abbreviations}"

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
└── {Unity Engine Abbreviations}"""


class TestCopy:  ###############################################################

    def test_copy1(_, testee1):
        copied = copy.copy(testee1)

        assert isinstance(copied, UnityEngineAbbrNode)
        assert copied.name == "{Unity Engine Abbreviations}"
        assert copied.parent is None

    def test_deep_copy1(_, testee1):
        copied = copy.deepcopy(testee1)

        assert isinstance(copied, UnityEngineAbbrNode)
        assert copied.name == "{Unity Engine Abbreviations}"
        assert copied.parent is None


class TestContentLines:  #######################################################

    def test1(_, testee1):
        opt = testee1.content_lines()
        print(opt)
        assert opt == ["- mb:MonoBehavior"]
