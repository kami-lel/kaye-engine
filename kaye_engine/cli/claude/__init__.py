"""
CLI subcommand for Anthropic Claude Skill & Plugin integration.
"""

from kaye_engine import LOGGER_NAME

# sublogger for all claude subcommands
LOGGER_CLAUDE_NAME = LOGGER_NAME + ".claude"

# sidecar names to auto-checkmark when exporting Claude prompts
CONTAINING_SIDECARS = ("for claude code", "prerequisite")

# name shown to Anthropic's plugin/marketplace tooling; set via
# set_claude_plugin_marketplace_name() in plugin_marketplace_name.py
PLUGIN_MARKETPLACE_NAME = None
