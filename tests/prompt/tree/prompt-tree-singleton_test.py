"""
prompt-tree-singleton_test.py

Unit Tests (using pytest) for:

load_prompt_corpus_tree
"""

from kaye_engine.prompt.prompt_corpus_loader import load_prompt_corpus_tree


# pytest  ######################################################################
class TestSingleton:

    def test1(_):
        attempt1 = load_prompt_corpus_tree()
        attempt2 = load_prompt_corpus_tree()
        attempt3 = load_prompt_corpus_tree()

        assert attempt1 is attempt2
        assert attempt2 is attempt3
