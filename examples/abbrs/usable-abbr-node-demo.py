"""
usable-abbr-node-demo.py

demonstrate ``UsableAbbrNode`` by building a single-node blueprint and
printing its generated prompt
"""

from kaye_engine.prompt import PromptBlueprint

# constants  ###################################################################
BLUEPRINT_TEXT = """ ○
[x] └── (Usable Abbreviations)"""


# Entry Point  #################################################################
if __name__ == "__main__":
    blueprint = PromptBlueprint.parse(BLUEPRINT_TEXT, disable_prune=True)
    prompt = blueprint.generate_prompt()
    print(prompt)
