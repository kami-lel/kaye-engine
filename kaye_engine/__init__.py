"""
Kaye Python Package API
"""

__all__ = (
    "LOGGER_NAME",
    "PACKAGE_NAME",
    "AbbrData",
    "get_default_corpus_tree",
    "load_corpus_tree",
    "populate_abbr_data_with_json_file",
    "register_abbr_glossary",
    "register_blueprint",
    "setup_claude_cli",
)


# installed distribution name, for importlib.metadata lookups
PACKAGE_NAME = "kaye-engine"
LOGGER_NAME = "kaye.engine"


# pylint: disable=wrong-import-position
from kaye_engine.abbr_collection import (
    AbbrData,
    populate_abbr_data_with_json_file,
    register_abbr_glossary,
)
from kaye_engine.cli.claude.setup import setup_claude_cli
from kaye_engine.prompt import (
    get_default_corpus_tree,
    load_corpus_tree,
    register_blueprint,
)
