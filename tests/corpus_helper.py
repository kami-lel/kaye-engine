"""
tests/corpus_helper.py

define ``load_corpus_from_sources`` -- register each source under the
root, then load the tree, for tests building a corpus from a list
"""

from kaye_engine.prompt.prompt_corpus_loader import (
    load_corpus_tree,
    register_corpus_under_node,
)

__all__ = ("load_corpus_from_sources",)


def load_corpus_from_sources(sources):
    """
    :param sources: sources to register under the root, in order
    :type sources: list[str or Path]
    :return: **root** node of the loaded corpus tree
    :rtype: PromptCorpusNode
    """
    for source in sources:
        register_corpus_under_node((), source)
    return load_corpus_tree()
