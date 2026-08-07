"""
Kaye Python Package API
"""

__all__ = (
    "DISPLAY_NAME",
    "LOGGER_NAME",
    "PACKAGE_NAME",
    "AbbrData",
    "get_abbr_data",
    "get_abbr_glossary",
    "get_blueprint",
    "get_corpus_tree",
    "get_default_corpus_tree",
    "load_corpus_tree",
    "register_abbr_glossary",
    "register_blueprint",
    "setup_claude_cli",
)


DISPLAY_NAME = "Prompt Engineering Project Kaye Engine"

# installed distribution name, for importlib.metadata lookups
PACKAGE_NAME = "kaye-engine"
LOGGER_NAME = "kaye.engine"


# pylint: disable=wrong-import-position

from kaye_engine.abbr_collection import (
    AbbrData,
    get_abbr_data,
    get_abbr_glossary,
    register_abbr_glossary,
)
from kaye_engine.cli.claude.setup import setup_claude_cli
from kaye_engine.prompt import (
    get_blueprint,
    get_corpus_tree,
    get_default_corpus_tree,
    load_corpus_tree,
    register_blueprint,
)
