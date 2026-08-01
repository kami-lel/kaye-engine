"""
Kaye Python Package API
"""

from kaye_engine import kamilog

__all__ = (
    "DISPLAY_NAME",
    "PROGRAM_NAME",
    "PACKAGE_NAME",
    "get_corpus_tree",
    "load_corpus_tree",
    "get_default_corpus_tree",
    "AbbrData",
    "get_abbr_data",
    "get_blueprint",
    "register_blueprint",
)


PROGRAM_NAME = "kaye-engine"  # HACK consider remove or more specific
DISPLAY_NAME = "Prompt Engineering Project Kaye Engine"

# installed distribution name, for importlib.metadata lookups
PACKAGE_NAME = "kaye-engine"
LOGGER_NAME = "kaye.engine"

# HACK del logger, use logger name instead
logger = kamilog.getLogger(PROGRAM_NAME)


from kaye_engine.prompt import (  # noqa: I001
    load_corpus_tree,
    get_corpus_tree,
    get_default_corpus_tree,
    get_blueprint,
    register_blueprint,
)
from kaye_engine.abbr_collection import (  # noqa: I001
    AbbrData,
    get_abbr_data,
)
