"""
plugin_marketplace_name.py

define ``get_plugin_name``, ``get_marketplace_name``,
``check_setup_for_claude_cli``
"""

from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.consumer import get_consumer_canonical_name

__all__ = (
    "check_setup_for_claude_cli",
    "get_marketplace_name",
    "get_plugin_name",
)


# Public API  ##################################################################


def get_plugin_name():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``register_consumer(...)``
    :return: plugin name, the registered canonical name
    :rtype: str
    """
    return get_consumer_canonical_name()


def get_marketplace_name():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``register_consumer(...)``
    :return: marketplace name, the registered canonical name
    :rtype: str
    """
    return get_consumer_canonical_name()


def check_setup_for_claude_cli():
    """
    perform the generic corpus/registry check; the consumer identity is
    validated separately by ``get_consumer_canonical_name()``
    """
    check_corpus_setup_for_cli()
