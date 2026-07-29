"""
Kaye Python Package API
"""

from kaye_engine import kamilog

__all__ = (
    "DISPLAY_NAME",
    "PROGRAM_NAME",
    "get_corpus_tree",
    "load_corpus_tree",
)


PROGRAM_NAME = "kaye-engine"
DISPLAY_NAME = "Prompt Engineering Project Kaye Engine"


logger = kamilog.getLogger(PROGRAM_NAME)


from kaye_engine.prompt import load_corpus_tree, get_corpus_tree  # noqa: I001
