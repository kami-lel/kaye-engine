"""
abbrs-abbr_nodes-demo.py

demonstrate ``AbbrNode`` by building a single-node blueprint and
printing its generated prompt
"""

from kaye.prompt import PromptBlueprint
from kaye.kamilog import gen_comment_banner_centered

# constants  ###################################################################
BLUEPRINT_TEXT = """ ○
[x] └── (Abbreviations)"""


# Entry Point  #################################################################
if __name__ == "__main__":
    # provided query  ==========================================================
    print(gen_comment_banner_centered("provided query", 1))
    print(gen_comment_banner_centered("abbr node content", 2))

    # empty query  =============================================================
    print("\n" + gen_comment_banner_centered("empty query", 1))
    print(gen_comment_banner_centered("abbr node content", 2))

    blueprint = PromptBlueprint.parse(BLUEPRINT_TEXT, disable_prune=True)
    prompt = blueprint.generate_prompt(
        disable_first_heading=True,
    )
    print(prompt)


# TODO demo to gen using query
