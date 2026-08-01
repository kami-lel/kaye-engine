"""
plugin_marketplace_name.py

define ``set_claude_plugin_marketplace_name``, ``check_setup_for_claude_cli``
"""

from kaye_engine import kamilog
from kaye_engine.cli import claude
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli

__all__ = (
    "check_setup_for_claude_cli",
    "set_claude_plugin_marketplace_name",
)

# logger  ######################################################################
logger = kamilog.getLogger(claude.LOGGER_CLAUDE_NAME)


# Public API  ##################################################################


def set_claude_plugin_marketplace_name(name):
    """
    set the name shown to Anthropic's plugin/marketplace tooling

    :param name: plugin/marketplace name,
            used in manifest and folder name generation
    :type name: str
    """
    claude.PLUGIN_MARKETPLACE_NAME = name


def check_setup_for_claude_cli():
    """
    warn when no host project has set a plugin/marketplace name, and
    perform the generic corpus/registry check as well
    """
    check_corpus_setup_for_cli()

    if claude.PLUGIN_MARKETPLACE_NAME is None:
        logger.warning(
            "no PLUGIN_MARKETPLACE_NAME set\n"
            "a host project should call "
            "set_claude_plugin_marketplace_name(...) before invoking this CLI"
        )
