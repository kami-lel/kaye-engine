"""
blueprint_name.py

define ``set_claude_using_blueprint``, ``get_claude_chat_blueprint``,
``get_claude_coder_blueprint``
"""

from kaye_engine import kamilog
from kaye_engine.cli import claude
from kaye_engine.prompt.blueprint import blueprint_registry

__all__ = (
    "get_claude_chat_blueprint",
    "get_claude_coder_blueprint",
    "set_claude_using_blueprint",
)

# logger  ######################################################################
logger = kamilog.getLogger(claude.LOGGER_CLAUDE_NAME)


# Public API  ##################################################################


def set_claude_using_blueprint(chat_bp_name, coder_bp_name):
    """
    set the registered blueprint names used for Claude user/system prompt
    export

    :param chat_bp_name: registered name of the Chat blueprint
    :type chat_bp_name: str
    :param coder_bp_name: registered name of the Coder blueprint
    :type coder_bp_name: str
    """
    claude._chat_blueprint_name = chat_bp_name
    claude._coder_blueprint_name = coder_bp_name


def _get_registered_blueprint(name):
    try:
        return blueprint_registry[name].blueprint
    except KeyError as err:
        logger.critical("unknown blueprint:\t" + str(name))
        raise SystemExit(1) from err


def get_claude_chat_blueprint():
    """
    return the Chat blueprint currently configured for export

    fails loudly instead of letting an unset name reach the blueprint
    registry lookup

    :return: the configured Chat blueprint
    :rtype: PromptBlueprint
    :raises SystemExit: exit code 1, when no consumer project has called
            ``set_claude_using_blueprint(...)``, or the configured name is
            not a registered blueprint
    """
    if claude._chat_blueprint_name is None:
        logger.critical(
            "no Chat blueprint name set\n"
            "a consumer project should call "
            "set_claude_using_blueprint(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return _get_registered_blueprint(claude._chat_blueprint_name)


def get_claude_coder_blueprint():
    """
    return the Coder blueprint currently configured for export

    fails loudly instead of letting an unset name reach the blueprint
    registry lookup

    :return: the configured Coder blueprint
    :rtype: PromptBlueprint
    :raises SystemExit: exit code 1, when no consumer project has called
            ``set_claude_using_blueprint(...)``, or the configured name is
            not a registered blueprint
    """
    if claude._coder_blueprint_name is None:
        logger.critical(
            "no Coder blueprint name set\n"
            "a consumer project should call "
            "set_claude_using_blueprint(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return _get_registered_blueprint(claude._coder_blueprint_name)
