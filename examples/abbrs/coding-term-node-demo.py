"""
coding-term-node-demo.py

demonstrate ``CodingTermsNode`` by building a single-node blueprint and
printing its generated prompt
"""

# Bug predates the corpus split; parses with no corpus_tree, so this
# script dies on "no default corpus tree set"
from kaye_engine.prompt import PromptBlueprint

# constants  ###################################################################
BLUEPRINT_TEXT = """ ○
[x] └── (Coding Terms)"""


# Entry Point  #################################################################
if __name__ == "__main__":
    blueprint = PromptBlueprint.parse(BLUEPRINT_TEXT, disable_prune=True)
    prompt = blueprint.generate_prompt()
    print(prompt)
