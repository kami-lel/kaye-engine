"""
CLI subcommand for Continue AI rule & prompt integration.
"""

from kaye_engine import LOGGER_NAME

# constants  ###################################################################

# sublogger for the continue subcommand
LOGGER_CONTINUE_NAME = LOGGER_NAME + ".continue"

# appended to the continue subcommand's help description
CONTINUE_DOC_DESCRIPTION = """

CONTINUE DOCUMENTATION:

see the continue command documentation on GitHub:

    https://github.com/kami-lel/kaye-engine/blob/main/docs/cli/continue-doc.md"""
