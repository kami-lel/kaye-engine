"""
CLI subcommand for Anthropic Claude Skill & Plugin integration.
"""

from kaye_engine import LOGGER_NAME

# constants  ###################################################################

# sublogger for all claude subcommands
LOGGER_CLAUDE_NAME = LOGGER_NAME + ".claude"

# name written into plugin.json / used as the plugin's folder name
_plugin_name = None

# display name stamped into plugin.json's display_name field
_display_name = None

# name written into marketplace.json
_marketplace_name = None

# registered exportable names used for Claude user/system prompt export
_chat_exportable_name = None
_chat_coder_exportable_name = None

# version stamped into plugin.json, marketplace.json, and every SKILL.md
_version = None

# folder name used for the marketplace under ~/.claude and under a given Claude folder
_marketplace_folder_name = None
