"""
create_blueprint.py

common blueprints creations
"""

from kaye.prompt.prompt_blueprint import PromptBlueprint

__all__ = (
    "create_rapid_blueprint",
    "create_chat_blueprint",
    "create_date_time_blueprint",
    "create_number_unit_blueprint",
)


# pylint: disable=missing-function-docstring


# Blueprints  ##################################################################


RAPID_PROMPT_BLUEPRINT = """    ○
[x] ├── Introduction
[x] ├── Format
[x] └── {Abbreviations}"""


CHAT_PROMPT_BLUEPRINT = """    ○
[x] ├── Introduction
[x] ├── Personality
[x] ├── Language
[x] ├── Format
[x] ├── Role
[x] └── {Abbreviations}"""


# creations  ###################################################################


def create_rapid_blueprint():
    return PromptBlueprint.parse(RAPID_PROMPT_BLUEPRINT)


def create_chat_blueprint():
    return PromptBlueprint.parse(CHAT_PROMPT_BLUEPRINT)


def create_date_time_blueprint():
    return PromptBlueprint.parse("""    ○
[x] └── Elements
[x]     └── Date & Time Format""")


def create_number_unit_blueprint():
    return PromptBlueprint.parse("""    ○
[x] └── Elements
[x]     └── Numerical Values with Units""")
