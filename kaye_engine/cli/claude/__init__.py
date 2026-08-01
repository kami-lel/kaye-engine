"""
CLI subcommand for Anthropic Claude Skill & Plugin integration.

define ``check_setup_for_claude_cli``
"""

from kaye_engine import LOGGER_NAME, kamilog

# constants  ###################################################################

# sublogger for all claude subcommands
LOGGER_CLAUDE_NAME = LOGGER_NAME + ".claude"

# sidecar names to auto-checkmark when exporting Claude prompts
CONTAINING_SIDECARS = ("for claude code", "prerequisite")

# name shown to Anthropic's plugin/marketplace tooling; set via
# set_claude_plugin_marketplace_name() in plugin_marketplace_name.py
PLUGIN_MARKETPLACE_NAME = None


# Public API  ###################################################################
def check_setup_for_claude_cli():
    """
    warn when no host project has set a plugin/marketplace name
    """
    logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)
    if PLUGIN_MARKETPLACE_NAME is None:
        logger.warning(
            "no PLUGIN_MARKETPLACE_NAME set\n"
            "a host project should call "
            "set_claude_plugin_marketplace_name(...) before invoking this CLI"
        )
