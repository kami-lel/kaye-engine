"""
setup.py

define ``setup_claude_cli``, ``get_claude_cli_consumer_version``,
``get_marketplace_folder_name``
"""

# pylint: disable=protected-access


from kaye_engine import kamilog
from kaye_engine.cli import claude
from kaye_engine.cli.claude.claude_affordances import (
    register_claude_affordances,
)

__all__ = (
    "get_claude_cli_consumer_version",
    "get_claude_cli_display_name",
    "get_marketplace_folder_name",
    "setup_claude_cli",
)

# logger  ######################################################################
logger = kamilog.getLogger(claude.LOGGER_CLAUDE_NAME)


# Public API  ##################################################################


def setup_claude_cli(
    plugin_name,
    display_name,
    marketplace_name,
    chat_exportable_name,
    chat_coder_exportable_name,
    version,
    marketplace_folder_name,
):
    """
    set every consumer-configurable value used by the ``claude`` CLI
    subcommand family in one call

    Prerequisite: :func:`register_exportable_entry` (or
    :func:`register_blueprint`) for ``chat_exportable_name`` and
    ``chat_coder_exportable_name``


    :param plugin_name: name written into ``plugin.json``, and used as the
            plugin's folder name and export keyword
    :type plugin_name: str
    :param display_name: display name stamped into ``plugin.json``'s
            ``display_name`` field
    :type display_name: str
    :param marketplace_name: name written into ``marketplace.json``
    :type marketplace_name: str
    :param chat_exportable_name: registered name, in
            `exportable_registry`, of the Chat exportable
    :type chat_exportable_name: str
    :param chat_coder_exportable_name: registered name, in
            `exportable_registry`, of the precomputed Chat+Coder
            exportable, used to build the final ``-c`` prompt
            (``usp -c``, ``claude code``, ``claude vs-code-extension``)
    :type chat_coder_exportable_name: str
    :param version: version string stamped into ``plugin.json``,
            ``marketplace.json``, and every exported ``SKILL.md``
    :type version: str
    :param marketplace_folder_name: folder name used for the marketplace,
            under ``~/.claude`` for ``claude marketplace``'s default
            destination, and under the target Claude folder for ``claude
            vs-code-extension``
    :type marketplace_folder_name: str
    """
    claude._plugin_name = plugin_name
    claude._display_name = display_name
    claude._marketplace_name = marketplace_name
    claude._chat_exportable_name = chat_exportable_name
    claude._chat_coder_exportable_name = chat_coder_exportable_name
    claude._version = version
    claude._marketplace_folder_name = marketplace_folder_name

    register_claude_affordances()


def get_claude_cli_consumer_version():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_claude_cli(...)``
    :return: configured version string
    :rtype: str
    """
    if claude._version is None:
        logger.critical(
            "no version set\n"
            "a consumer project should call "
            "setup_claude_cli(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return claude._version


def get_claude_cli_display_name():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_claude_cli(...)``
    :return: configured display name
    :rtype: str
    """
    if claude._display_name is None:
        logger.critical(
            "no display name set\n"
            "a consumer project should call "
            "setup_claude_cli(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return claude._display_name


def get_marketplace_folder_name():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_claude_cli(...)``
    :return: configured marketplace folder name
    :rtype: str
    """
    if claude._marketplace_folder_name is None:
        logger.critical(
            "no marketplace folder name set\n"
            "a consumer project should call "
            "setup_claude_cli(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return claude._marketplace_folder_name
