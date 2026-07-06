"""
abbrs-coding_term_node-demo.py

demonstrate ``CodingTermsNode`` by building a single-node blueprint and
printing its generated prompt
"""

from kaye.prompt import PromptBlueprint

# constants  ###################################################################
BLUEPRINT_TEXT = """ ○
[x] └── (Coding Terms)"""


# Entry Point  #################################################################
if __name__ == "__main__":
    blueprint = PromptBlueprint.parse(BLUEPRINT_TEXT, disable_prune=True)
    prompt = blueprint.generate_prompt()
    print(prompt)
