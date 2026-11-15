"""
exportable_name.py

define ``get_codex_chat_exportable``, ``get_codex_merged_coder_exportable``
"""

# pylint: disable=protected-access

import kamilog
from kaye_engine.cli import codex
from kaye_engine.exportable import get_exportable

__all__ = (
    "get_codex_chat_exportable",
    "get_codex_merged_coder_exportable",
)

# logger  ######################################################################
logger = kamilog.getLogger(codex.LOGGER_CODEX_NAME)


def _get_configured_exportable(name, label):
    if name is None:
        logger.critical(
            "no {} exportable name set\n"
            "a consumer project should call "
            "setup_codex_cli(...) before invoking this CLI".format(label)
        )
        raise SystemExit(1)
    try:
        return get_exportable(name)
    except KeyError as err:
        logger.critical("unknown exportable:\t" + str(name))
        raise SystemExit(1) from err


# Public API  ##################################################################


def get_codex_chat_exportable():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_codex_cli(...)``, or the configured name is not a
            registered exportable
    :return: the configured Chat exportable
    :rtype: Exportable
    """
    return _get_configured_exportable(codex._chat_exportable_name, "Chat")


def get_codex_merged_coder_exportable():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_codex_cli(...)``, or the configured name is not a
            registered exportable
    :return: the configured merged Coder exportable, the Coder carrying
            Chat as a dependency
    :rtype: Exportable
    """
    return _get_configured_exportable(
        codex._merged_coder_exportable_name, "merged Coder"
    )
