"""
CLI subcommand for exporting a Hermes home directory.
"""

from kaye_engine import LOGGER_NAME

# constants  ###################################################################

# sublogger for the hermes subcommand
LOGGER_HERMES_NAME = LOGGER_NAME + ".hermes"

# folder name, under ``skills/``, that holds every exported skill
_skill_category = None

# registered blueprint name rendered into the root ``SOUL.md``
_soul_blueprint_name = None

# profile name -> registered blueprint name rendered into
# ``profiles/<name>/SOUL.md``
_profile_blueprint_names = None
