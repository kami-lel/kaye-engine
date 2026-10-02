"""
CLI subcommand for exporting a Hermes home directory.
"""

from kaye_engine import LOGGER_NAME

# constants  ###################################################################

# sublogger for the hermes subcommand
LOGGER_HERMES_NAME = LOGGER_NAME + ".hermes"

# appended to the hermes subcommand's help description
HERMES_DOC_DESCRIPTION = """

see support for Hermes on Github:

    https://github.com/kami-lel/kaye-engine/blob/main/docs/hermes-doc.md"""

# registered blueprint name rendered into the root ``SOUL.md``
_soul_blueprint_name = None

# profile name -> registered blueprint name rendered into
# ``profiles/<name>/SOUL.md``
_profile_blueprint_names = None
