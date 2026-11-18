"""
plugin_marketplace_name.py

define ``get_marketplace_name``, ``check_setup_for_claude_cli``
"""

from kaye_engine.cli.plugin_platform.consumers import (
    check_setup_for_plugin_cli,
)
from kaye_engine.repo import get_repo_name

__all__ = (
    "check_setup_for_claude_cli",
    "get_marketplace_name",
)


# Public API  ##################################################################


def get_marketplace_name():
    """
    :raises SystemExit: exit code 1, when the repo name is unset
    :return: marketplace name, the repo name the consumer project
            registered with ``set_repo_name``: each repo's commands write
            a marketplace of their own, listing one plugin per consumer
    :rtype: str
    """
    return get_repo_name()


def check_setup_for_claude_cli():
    """
    perform the setup check every ``claude`` subcommand runs first, ie
    :func:`check_setup_for_plugin_cli`


    :raises SystemExit: exit code 1, when no consumer is registered, as on
            a bare checkout, so there is no plugin to write
    """
    check_setup_for_plugin_cli()
