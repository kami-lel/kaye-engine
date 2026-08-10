"""
CLI subcommand for Anthropic Claude Skill & Plugin integration.
"""

from kaye_engine import LOGGER_NAME

# constants  ###################################################################

# sublogger for all claude subcommands
LOGGER_CLAUDE_NAME = LOGGER_NAME + ".claude"

# sidecar names to auto-checkmark per Claude export surface
CLAUDE_CHAT_SIDECARS = ()
CLAUDE_COWORK_SIDECARS = ()
CLAUDE_CODE_SIDECARS = (
    "Claude Tool:Enter/ExitPlanMode",
    "Claude Tool:TodoWrite",
    "Claude Tool:AskUserQuestion",
    "Claude Tool:Subagents",
    "Claude Tool:Tasks",
    "Claude Tool:Worktrees",
    "Claude Tool:Skill",
    "Claude Tool:Workflow",
    "Claude Tool:ReportFindings",
)
CLAUDE_CODE_VSC_XTN_SIDECARS = (
    "Claude Tool:Enter/ExitPlanMode",
    "Claude Tool:TodoWrite",
    "Claude Tool:AskUserQuestion",
    "Claude Tool:Subagents",
    "Claude Tool:Tasks",
    "Claude Tool:Worktrees",
    "Claude Tool:Skill",
    "Claude Tool:Workflow",
    "Claude Tool:ReportFindings",
)

# name written into plugin.json / used as the plugin's folder name
_plugin_name = None

# display name stamped into plugin.json's display_name field
_display_name = None

# name written into marketplace.json
_marketplace_name = None

# registered blueprint names used for Claude user/system prompt export
_chat_blueprint_name = None
_coder_blueprint_name = None

# version stamped into plugin.json, marketplace.json, and every SKILL.md
_version = None

# folder name used for the marketplace under ~/.claude and under a given Claude folder
_marketplace_folder_name = None
