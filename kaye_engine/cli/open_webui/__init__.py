"""
CLI subcommand for pushing exportables into Open WebUI as skills.
"""

from kaye_engine import LOGGER_NAME

# constants  ###################################################################

# sublogger for the sync-open-webui-skills subcommand
LOGGER_OPEN_WEBUI_NAME = LOGGER_NAME + ".open-webui"

# appended to the sync-open-webui-skills subcommand's help description
OPEN_WEBUI_DOC_DESCRIPTION = """

OPEN WEBUI DOCUMENTATION:

see the sync-open-webui-skills command documentation on GitHub:

    https://github.com/kami-lel/kaye-engine/blob/main/docs/cli/open-webui-doc.md"""
