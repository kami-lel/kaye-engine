"""
plugin_marketplace_name.py

define ``get_marketplace_name``, ``get_plugin_consumers``,
``check_setup_for_claude_cli``
"""

from kaye_engine import PACKAGE_NAME
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.consumer import iter_consumers
from kaye_engine.exportable import exportable_registry

__all__ = (
    "check_setup_for_claude_cli",
    "get_marketplace_name",
    "get_plugin_consumers",
)


# Public API  ##################################################################


def get_marketplace_name():
    """
    :return: marketplace name, always the engine's own name: one
            marketplace lists one plugin per consumer
    :rtype: str
    """
    return PACKAGE_NAME


def get_plugin_consumers():
    """
    :return: every registered consumer holding at least one exportable,
            each of which is one plugin
    :rtype: tuple[Consumer, ...]
    """
    holders = {e.consumer for e in exportable_registry.values()}
    return tuple(c for c in iter_consumers() if c.canonical_name in holders)


def check_setup_for_claude_cli():
    """
    perform the generic corpus/registry check; the entry consumer is
    validated separately by the ``get_consumer_*`` getters
    """
    check_corpus_setup_for_cli()
