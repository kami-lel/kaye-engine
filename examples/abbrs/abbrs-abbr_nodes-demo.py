"""
abbrs-abbr_nodes-demo.py

demonstrate ``AbbrNode`` by building a single-node blueprint and
printing its generated prompt
"""

from kaye.prompt import PromptBlueprint

# constants  ###################################################################
BLUEPRINT_TEXT = """ ○
[x] └── (Abbreviations)"""


# Entry Point  #################################################################
if __name__ == "__main__":
    blueprint = PromptBlueprint.parse(BLUEPRINT_TEXT, disable_prune=True)
    prompt = blueprint.generate_prompt(
        disable_first_heading=True,
    )
    print(prompt)


# Todo demo to gen using query
