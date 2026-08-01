"""
CLI subcommand for Anthropic Claude Skill & Plugin integration.
"""

from kaye_engine import LOGGER_NAME

# sublogger for all claude subcommands
LOGGER_CLAUDE_NAME = LOGGER_NAME + ".claude"

# sidecar names to auto-checkmark when exporting Claude prompts
CONTAINING_SIDECARS = ("for claude code", "prerequisite")

# name shown to Anthropic's plugin/marketplace tooling
# FIXME set plugin/marketplace name by api
PLUGIN_MARKETPLACE_NAME = "kaye"
