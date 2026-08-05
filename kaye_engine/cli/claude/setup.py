"""
setup.py

define ``setup_claude_cli``, ``get_claude_cli_version``,
``get_marketplace_folder_name``
"""

# pylint: disable=protected-access


from kaye_engine import kamilog
from kaye_engine.cli import claude

__all__ = (
    "get_claude_cli_version",
    "get_marketplace_folder_name",
    "setup_claude_cli",
)

# logger  ######################################################################
logger = kamilog.getLogger(claude.LOGGER_CLAUDE_NAME)


# Public API  ##################################################################


def setup_claude_cli(
    plugin_name,
    marketplace_name,
    chat_bp_name,
    coder_bp_name,
    version,
    marketplace_folder_name,
):
    """
    set every consumer-configurable value used by the ``claude`` CLI
    subcommand family in one call

    :param plugin_name: name written into ``plugin.json``, and used as the
            plugin's folder name and export keyword
    :type plugin_name: str
    :param marketplace_name: name written into ``marketplace.json``
    :type marketplace_name: str
    :param chat_bp_name: registered name of the Chat blueprint
    :type chat_bp_name: str
    :param coder_bp_name: registered name of the Coder blueprint
    :type coder_bp_name: str
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
    claude._marketplace_name = marketplace_name
    claude._chat_blueprint_name = chat_bp_name
    claude._coder_blueprint_name = coder_bp_name
    claude._version = version
    claude._marketplace_folder_name = marketplace_folder_name


def get_claude_cli_version():
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
