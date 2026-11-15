"""
platform-neutral plugin plumbing shared by every plugin platform (Claude,
Codex): consumer selection and package metadata
"""

from kaye_engine import LOGGER_NAME

# constants  ###################################################################

# sublogger for platform-neutral plugin plumbing
LOGGER_PLUGIN_PLATFORM_NAME = LOGGER_NAME + ".plugin"
