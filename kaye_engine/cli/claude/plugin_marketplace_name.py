"""
plugin_marketplace_name.py

define ``set_claude_plugin_marketplace_name``, ``get_plugin_marketplace_name``,
``check_setup_for_claude_cli``
"""

from kaye_engine import kamilog
from kaye_engine.cli import claude
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli

__all__ = (
    "check_setup_for_claude_cli",
    "get_plugin_marketplace_name",
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
    claude._plugin_marketplace_name = name


def get_plugin_marketplace_name():
    """
    return the name shown to Anthropic's plugin/marketplace tooling

    fails loudly instead of letting an unset name reach path/string
    building, where it previously surfaced as a ``TypeError`` or a
    silently malformed ``"./plugins/None"`` source path

    :return: plugin/marketplace name
    :rtype: str
    :raises SystemExit: exit code 1, when no consumer project has called
            ``set_claude_plugin_marketplace_name(...)``
    """
    if claude._plugin_marketplace_name is None:
        logger.critical(
            "no PLUGIN_MARKETPLACE_NAME set\n"
            "a consumer project should call "
            "set_claude_plugin_marketplace_name(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return claude._plugin_marketplace_name


def check_setup_for_claude_cli():
    """
    perform the generic corpus/registry check; the plugin/marketplace
    name is validated separately by ``get_plugin_marketplace_name()``
    """
    check_corpus_setup_for_cli()
