"""
plugin_marketplace_name.py

define ``get_plugin_name``, ``get_marketplace_name``,
``check_setup_for_claude_cli``
"""

from kaye_engine import kamilog
from kaye_engine.cli import claude
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli

__all__ = (
    "check_setup_for_claude_cli",
    "get_marketplace_name",
    "get_plugin_name",
)

# logger  ######################################################################
logger = kamilog.getLogger(claude.LOGGER_CLAUDE_NAME)


# Public API  ##################################################################


def get_plugin_name():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_claude_cli(...)``
    :return: plugin name
    :rtype: str
    """
    if claude._plugin_name is None:
        logger.critical(
            "no PLUGIN_NAME set\n"
            "a consumer project should call "
            "setup_claude_cli(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return claude._plugin_name


def get_marketplace_name():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_claude_cli(...)``
    :return: marketplace name
    :rtype: str
    """
    if claude._marketplace_name is None:
        logger.critical(
            "no MARKETPLACE_NAME set\n"
            "a consumer project should call "
            "setup_claude_cli(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return claude._marketplace_name


def check_setup_for_claude_cli():
    """
    perform the generic corpus/registry check; the plugin and marketplace
    names are validated separately by ``get_plugin_name()`` and
    ``get_marketplace_name()``
    """
    check_corpus_setup_for_cli()
