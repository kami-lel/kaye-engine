"""
CLI subcommand for OpenAI Codex plugin & marketplace integration.
"""

from kaye_engine import LOGGER_NAME

# constants  ###################################################################

# appended to every codex subcommand's help description
CODEX_DOC_DESCRIPTION = """

see support for OpenAI Codex on Github:

    https://github.com/kami-lel/kaye-engine/blob/main/docs/codex-doc.md"""

# sublogger for all codex subcommands
LOGGER_CODEX_NAME = LOGGER_NAME + ".codex"

# registered exportable names used for the Codex AGENTS.md prompt export
_chat_exportable_name = None
_merged_coder_exportable_name = None
