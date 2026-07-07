"""
abbr-node-empty-query-demo.py

demonstrate ``AbbrNode`` with an empty ``query``, building a
single-node blueprint and printing its generated prompt
"""

from kaye.prompt import PromptBlueprint

# constants  ###################################################################
BLUEPRINT_TEXT = """ ○
[x] └── (Abbreviations)"""


# Entry Point  #################################################################
if __name__ == "__main__":
    blueprint = PromptBlueprint.parse(BLUEPRINT_TEXT, disable_prune=True)

    prompt = blueprint.generate_prompt()
    print(prompt)
