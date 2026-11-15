"""
setup.py

define ``setup_codex_cli``
"""

# pylint: disable=protected-access

from kaye_engine.cli import codex

__all__ = ("setup_codex_cli",)


def setup_codex_cli(
    chat_exportable_name=None,
    merged_coder_exportable_name=None,
):
    """
    set every consumer-configurable value used by the ``codex`` CLI
    subcommand family in one call

    Prerequisite: :func:`register_consumer` for each consumer and
    :func:`set_entry_consumer`, and :func:`register_exportable_entry` (or
    :func:`register_blueprint`) for both names when given; ``codex
    user-system-prompt`` needing an unset name exits 1 with a clear
    message


    :param chat_exportable_name: registered name, in
            `exportable_registry`, of the Chat exportable
    :type chat_exportable_name: str or None, optional
    :param merged_coder_exportable_name: registered name, in
            `exportable_registry`, of the Coder exportable carrying
            Chat as a dependency, used to build the ``-c`` prompt
    :type merged_coder_exportable_name: str or None, optional
    """
    codex._chat_exportable_name = chat_exportable_name
    codex._merged_coder_exportable_name = merged_coder_exportable_name
