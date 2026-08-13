"""
blueprint_name.py

define ``get_claude_chat_blueprint``, ``get_claude_coder_blueprint``
"""

from kaye_engine import kamilog
from kaye_engine.cli import claude
from kaye_engine.prompt.blueprint import blueprint_registry

__all__ = (
    "get_claude_chat_blueprint",
    "get_claude_coder_blueprint",
)

# logger  ######################################################################
logger = kamilog.getLogger(claude.LOGGER_CLAUDE_NAME)


# Public API  ##################################################################


def _get_registered_blueprint(name):
    try:
        return blueprint_registry[name].blueprint
    except KeyError as err:
        logger.critical("unknown blueprint:\t" + str(name))
        raise SystemExit(1) from err


def get_claude_chat_blueprint():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_claude_cli(...)``, or the configured name is not a
            registered blueprint
    :return: the configured Chat blueprint
    :rtype: PromptBlueprint
    """
    if claude._chat_blueprint_name is None:
        logger.critical(
            "no Chat blueprint name set\n"
            "a consumer project should call "
            "setup_claude_cli(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return _get_registered_blueprint(claude._chat_blueprint_name)


def get_claude_coder_blueprint():
    """
    the returned blueprint is meant to be merged into the Chat blueprint
    (via ``|``) to build the final ``-c`` prompt; see ``coder_bp_name``
    on :func:`kaye_engine.cli.claude.setup.setup_claude_cli`

    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_claude_cli(...)``, or the configured name is not a
            registered blueprint
    :return: the configured Coder blueprint
    :rtype: PromptBlueprint
    """
    if claude._coder_blueprint_name is None:
        logger.critical(
            "no Coder blueprint name set\n"
            "a consumer project should call "
            "setup_claude_cli(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return _get_registered_blueprint(claude._coder_blueprint_name)
