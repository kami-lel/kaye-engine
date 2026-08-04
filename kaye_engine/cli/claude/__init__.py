"""
CLI subcommand for Anthropic Claude Skill & Plugin integration.
"""

from kaye_engine import LOGGER_NAME

# constants  ###################################################################

# sublogger for all claude subcommands
LOGGER_CLAUDE_NAME = LOGGER_NAME + ".claude"

# sidecar names to auto-checkmark when exporting Claude prompts
CONTAINING_SIDECARS = ("for claude code", "prerequisite")

# name shown to Anthropic's plugin/marketplace tooling
_plugin_marketplace_name = None

# registered blueprint names used for Claude user/system prompt export
_chat_blueprint_name = None
_coder_blueprint_name = None
