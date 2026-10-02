"""
CLI subcommand for Anthropic Claude plugin & marketplace integration.
"""

from kaye_engine import LOGGER_NAME

# constants  ###################################################################

# appended to every claude subcommand's help description
CLAUDE_DOC_DESCRIPTION = """

see support for Anthropic Claude on Github:

    https://github.com/kami-lel/kaye-engine/blob/main/docs/claude-doc.md"""

# sublogger for all claude subcommands
LOGGER_CLAUDE_NAME = LOGGER_NAME + ".claude"

# registered exportable names used for Claude user/system prompt export
_chat_exportable_name = None
_merged_coder_exportable_name = None

# affordance name -> its variant names for register_claude_affordances()
_affordance_groups = {}

# dict[str, RenderProfile] populating the --surface flag's choices;
# None when the consumer project never configured surfaces
_surface_profiles = None
