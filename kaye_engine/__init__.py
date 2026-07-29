"""
Kaye Python Package API
"""

from kaye_engine import kamilog

__all__ = (
    "DISPLAY_NAME",
    "PROGRAM_NAME",
    "get_corpus_tree",
    "load_corpus_tree",
    "get_blueprint",
    "register_blueprint",
)


PROGRAM_NAME = "kaye-engine"
DISPLAY_NAME = "Prompt Engineering Project Kaye Engine"


logger = kamilog.getLogger(PROGRAM_NAME)


from kaye_engine.prompt import (  # noqa: I001
    load_corpus_tree,
    get_corpus_tree,
    get_blueprint,
    register_blueprint,
)
