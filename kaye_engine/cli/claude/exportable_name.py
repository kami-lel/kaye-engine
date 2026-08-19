"""
exportable_name.py

define ``get_claude_chat_exportable``, ``get_claude_chat_coder_exportable``
"""

# pylint: disable=protected-access

from kaye_engine import kamilog
from kaye_engine.cli import claude
from kaye_engine.exportable import get_exportable

__all__ = (
    "get_claude_chat_exportable",
    "get_claude_chat_coder_exportable",
)

# logger  ######################################################################
logger = kamilog.getLogger(claude.LOGGER_CLAUDE_NAME)


# Public API  ##################################################################


def _get_registered_exportable(name):
    try:
        return get_exportable(name)
    except KeyError as err:
        logger.critical("unknown exportable:\t" + str(name))
        raise SystemExit(1) from err


def get_claude_chat_exportable():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_claude_cli(...)``, or the configured name is not a
            registered exportable
    :return: the configured Chat exportable
    :rtype: Exportable
    """
    if claude._chat_exportable_name is None:
        logger.critical(
            "no Chat exportable name set\n"
            "a consumer project should call "
            "setup_claude_cli(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return _get_registered_exportable(claude._chat_exportable_name)


def get_claude_chat_coder_exportable():
    """
    the returned exportable is the precomputed merge of Chat and Coder,
    used to build the final ``-c`` prompt; see
    ``chat_coder_exportable_name`` on
    :func:`kaye_engine.cli.claude.setup.setup_claude_cli`

    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_claude_cli(...)``, or the configured name is not a
            registered exportable
    :return: the configured Chat Coder exportable
    :rtype: Exportable
    """
    if claude._chat_coder_exportable_name is None:
        logger.critical(
            "no Chat Coder exportable name set\n"
            "a consumer project should call "
            "setup_claude_cli(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return _get_registered_exportable(claude._chat_coder_exportable_name)
