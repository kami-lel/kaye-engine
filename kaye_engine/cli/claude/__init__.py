"""
CLI subcommand for Anthropic Claude Skill & Plugin integration.
"""

from kaye_engine import PROGRAM_NAME

# sidecar names to auto-checkmark when exporting Claude prompts
CONTAINING_SIDECARS = ("for claude code", "prerequisite")

# name shown to Anthropic's plugin/marketplace tooling
PLUGIN_MARKETPLACE_NAME = PROGRAM_NAME
