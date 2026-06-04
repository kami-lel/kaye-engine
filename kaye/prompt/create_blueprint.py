"""
create_blueprint.py

common blueprints to use
"""

from kaye.prompt.prompt_blueprint import PromptBlueprint

__all__ = ("create_rapid_blueprint",)


# Blueprints  ##################################################################


RAPID_PROMPT_BLUEPRINT = """    ○
[x] ├── Introduction
[x] ├── Format
[x] └── {Abbreviations}"""


# creations  ###################################################################


def create_rapid_blueprint():
    return PromptBlueprint.parse(RAPID_PROMPT_BLUEPRINT)
