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
    "set_claude_plugin_marketplace_name",
    "set_claude_using_blueprint",
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
)
from kaye_engine.cli.claude.plugin_marketplace_name import (
    set_claude_plugin_marketplace_name,
)
from kaye_engine.cli.claude.blueprint_name import (
    set_claude_using_blueprint,
)
