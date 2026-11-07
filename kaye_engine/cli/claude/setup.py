"""
setup.py

define ``setup_claude_cli``, ``get_marketplace_folder_name``
"""

# pylint: disable=protected-access


import kamilog
from kaye_engine.cli import claude
from kaye_engine import PACKAGE_NAME

__all__ = (
    "get_marketplace_folder_name",
    "setup_claude_cli",
)

# logger  ######################################################################
logger = kamilog.getLogger(claude.LOGGER_CLAUDE_NAME)


# Public API  ##################################################################


def setup_claude_cli(
    chat_exportable_name=None,
    merged_coder_exportable_name=None,
):
    """
    set every consumer-configurable value used by the ``claude`` CLI
    subcommand family in one call

    Prerequisite: :func:`register_consumer` for each consumer and
    :func:`set_entry_consumer`, and :func:`register_exportable_entry` (or
    :func:`register_blueprint`) for ``chat_exportable_name`` and
    ``merged_coder_exportable_name`` when given; a subcommand needing an
    unset name (``code``, ``user-system-prompt``, ``vs-code-extension``)
    exits 1 with a clear message


    :param chat_exportable_name: registered name, in
            `exportable_registry`, of the Chat exportable
    :type chat_exportable_name: str or None, optional
    :param merged_coder_exportable_name: registered name, in
            `exportable_registry`, of the Coder exportable carrying
            Chat as a dependency, used to build the final ``-c``
            prompt (``usp -c``, ``claude code``, ``claude
            vs-code-extension``)
    :type merged_coder_exportable_name: str or None, optional
    """
    claude._chat_exportable_name = chat_exportable_name
    claude._merged_coder_exportable_name = merged_coder_exportable_name


def get_marketplace_folder_name():
    """
    :return: marketplace folder name, the marketplace name
    :rtype: str
    """
    return PACKAGE_NAME
