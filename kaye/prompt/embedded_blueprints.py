"""
embedded_blueprints.py

common blueprints creations
"""

from kaye.prompt.prompt_blueprint import PromptBlueprint

__all__ = (
    "rapid_blueprint",
    "chat_blueprint",
    "date_time_blueprint",
    "number_unit_blueprint",
)

# blueprints  ##################################################################

rapid_blueprint = PromptBlueprint.parse("""    ○
[x] ├── Introduction
[x] ├── Format
[x] └── {Abbreviations}""")

chat_blueprint = PromptBlueprint.parse("""    ○
[x] ├── Introduction
[x] ├── Personality
[x] ├── Language
[x] ├── Format
[x] ├── Role
[x] └── {Abbreviations}""")

date_time_blueprint = PromptBlueprint.parse("""    ○
[x] └── Elements
[x]     └── Date & Time Format""")

number_unit_blueprint = PromptBlueprint.parse("""    ○
[x] └── Elements
[x]     └── Numerical Values with Units""")
