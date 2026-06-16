"""
prompt-node-is_prerequisite_node_test.py

Unit Tests (using pytest) for: BasePromptNode:

- .is_prerequisite_node
"""

from kaye.prompt.prompt_corpus_node import PromptCorpusNode


class TestIsPrerequisiteNode:  #################################################

    def test_prerequisite_node(_):
        node = PromptCorpusNode("{prerequisite}", None, [])

        assert node.is_prerequisite_node is True

    def test_other_meta_node(_):
        node = PromptCorpusNode("{description}", None, [])

        assert node.is_prerequisite_node is False

    def test_regular_node(_):
        node = PromptCorpusNode("Some Node", None, [])

        assert node.is_prerequisite_node is False
