"""
create_blueprint.py

common blueprints creations
"""

from kaye.prompt.prompt_blueprint import PromptBlueprint

__all__ = ("create_rapid_blueprint", "create_chat_blueprint")


# Blueprints  ##################################################################


RAPID_PROMPT_BLUEPRINT = """    ○
[x] ├── Introduction
[x] ├── Format
[x] └── {Abbreviations}"""


CHAT_PROMPT_BLUEPRINT = """    ○
[x] ├── Introduction
[x] ├── Personality
[x] ├── Language
[x] ├── Elements
[x] │   ├── Date & Time Format
[x] │   └── Numerical Values with Units
[x] ├── Format
[x] ├── Role
[x] └── {Abbreviations}"""


# creations  ###################################################################


def create_rapid_blueprint():
    return PromptBlueprint.parse(RAPID_PROMPT_BLUEPRINT)


def create_chat_blueprint():
    return PromptBlueprint.parse(CHAT_PROMPT_BLUEPRINT)
