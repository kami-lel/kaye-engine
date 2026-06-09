"""
prompt-node-description_test.py

Unit Tests (using pytest) for:

- PromptCorpusNode.is_description_node
- PromptCorpusNode.description_subnode
"""

import pytest

# Pytest fixtures  #############################################################


@pytest.fixture
def testee_node(corpus_testee2):
    return corpus_testee2["Project Title"]["Contributing"]


@pytest.fixture
def testee_subnode(testee_node):
    return testee_node["description"]


# Pytest unit tests  ###########################################################


class TestIsDescriptionNode:  # ================================================

    def test1(_, testee_node):
        node = testee_node
        assert not node.is_description_node

    def test2(_, testee_subnode):
        node = testee_subnode
        assert node.is_description_node


class TestDescriptionSubnode:  # ===============================================

    def test1(_, testee_node, testee_subnode):
        assert testee_node.description_subnode is testee_subnode

    def test2(_, testee_subnode):
        assert testee_subnode.description_subnode is None
