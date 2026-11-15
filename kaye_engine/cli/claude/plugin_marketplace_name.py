"""
plugin_marketplace_name.py

define ``get_marketplace_name``, ``check_setup_for_claude_cli``
"""

from kaye_engine import PACKAGE_NAME
from kaye_engine.cli.plugin_platform.consumers import (
    check_setup_for_plugin_cli,
)

__all__ = (
    "check_setup_for_claude_cli",
    "get_marketplace_name",
)


# Public API  ##################################################################


def get_marketplace_name():
    """
    :return: marketplace name, always the engine's own name: one
            marketplace lists one plugin per consumer
    :rtype: str
    """
    return PACKAGE_NAME


def check_setup_for_claude_cli():
    """
    perform the setup check every ``claude`` subcommand runs first, ie
    :func:`check_setup_for_plugin_cli`


    :raises SystemExit: exit code 1, when no consumer is registered, as on
            a bare checkout, so there is no plugin to write
    """
    check_setup_for_plugin_cli()
