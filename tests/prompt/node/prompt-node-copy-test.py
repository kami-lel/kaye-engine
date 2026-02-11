"""
prompt-node-copy-test.py

Unit Tests (using pytest) for:

copy & deepcopy of PromptCorpusNode
"""

import copy


import pytest

# BUG BUG in deepcopy


# fixtures  ####################################################################
@pytest.fixture
def copy_testee1(corpus_testee1):
    return copy.copy(corpus_testee1)


@pytest.fixture
def deepcopy_testee1(corpus_testee1):
    return copy.deepcopy(corpus_testee1)


@pytest.fixture
def copy_testee3(corpus_testee3):
    return copy.copy(corpus_testee3)


@pytest.fixture
def deepcopy_testee3(corpus_testee3):
    return copy.deepcopy(corpus_testee3)


class TestPrompt1:  ############################################################

    def test_copy1(_, copy_testee1, corpus_testee1):
        copied = copy_testee1
        src = corpus_testee1

        assert copied.name == "○"
        assert copied._content_lines == src._content_lines
        assert len(copied.descendants) == 0

    def test_deepcopy1(_, corpus_testee1, deepcopy_testee1):
        copied = deepcopy_testee1
        src = corpus_testee1

        assert copied.name == "○"
        assert copied._content_lines == src._content_lines
        assert len(copied.descendants) == len(src.descendants)

    def test_deepcopy2(_, corpus_testee1, deepcopy_testee1):
        copied = deepcopy_testee1.children[0].children[1]
        src = corpus_testee1.children[0].children[1]

        assert copied.name == src.name
        assert copied._content_lines == src._content_lines
        assert len(copied.descendants) == len(src.descendants)


class TestPrompt3:  ############################################################

    def test_copy3(_, copy_testee3, corpus_testee3):
        copied = copy_testee3
        src = corpus_testee3

        assert copied.name == "○"
        assert copied._content_lines == src._content_lines
        assert len(copied.descendants) == 0

    def test_deepcopy3(_, corpus_testee3, deepcopy_testee3):
        copied = deepcopy_testee3
        src = corpus_testee3

        assert copied.name == "○"
        assert copied._content_lines == src._content_lines
        assert len(copied.descendants) == len(src.descendants)

    def test_deepcopy2(_, corpus_testee3, deepcopy_testee3):
        copied = deepcopy_testee3.children[0].children[3]
        src = corpus_testee3.children[0].children[3]

        assert copied.name == src.name
        assert copied._content_lines == src._content_lines
        assert len(copied.descendants) == len(src.descendants)
