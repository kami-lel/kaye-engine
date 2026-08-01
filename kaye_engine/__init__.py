"""
Kaye Python Package API
"""

__all__ = (
    "DISPLAY_NAME",
    "PACKAGE_NAME",
    "LOGGER_NAME",
    "get_corpus_tree",
    "load_corpus_tree",
    "get_default_corpus_tree",
    "AbbrData",
    "get_abbr_data",
    "get_blueprint",
    "register_blueprint",
)


DISPLAY_NAME = "Prompt Engineering Project Kaye Engine"

# installed distribution name, for importlib.metadata lookups
PACKAGE_NAME = "kaye-engine"
LOGGER_NAME = "kaye.engine"

# constants above must stay defined before these imports: kaye_engine.
# prompt.blueprint.render imports PACKAGE_NAME back from this module, and
# importing it first leaves that name undefined mid-initialization
from kaye_engine.prompt import (
    load_corpus_tree,
    get_corpus_tree,
    get_default_corpus_tree,
    get_blueprint,
    register_blueprint,
)
from kaye_engine.abbr_collection import (
    AbbrData,
    get_abbr_data,
)
