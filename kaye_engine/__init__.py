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
    "register_abbr_group",
    "get_abbr_group",
    "get_blueprint",
    "register_blueprint",
    "setup_claude_cli",
)


DISPLAY_NAME = "Prompt Engineering Project Kaye Engine"

# installed distribution name, for importlib.metadata lookups
PACKAGE_NAME = "kaye-engine"
LOGGER_NAME = "kaye.engine"

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
    register_abbr_group,
    get_abbr_group,
)
from kaye_engine.cli.claude.setup import setup_claude_cli
