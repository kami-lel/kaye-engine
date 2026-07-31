"""
abbr-node-provided-query-demo.py

demonstrate ``AbbrNode`` with a provided ``query``, building a
single-node blueprint and printing its generated prompt
"""

# Bug predates the corpus split; parses with no corpus_tree, so this
# script dies on "no default corpus tree set"
from kaye_engine.prompt import PromptBlueprint
from kaye_engine.kamilog import gen_comment_banner_centered

# constants  ###################################################################
BLUEPRINT_TEXT = """ ○
[x] └── (Abbreviations)"""

QUERY = (
    "The ind rev catalyzed a tectonic shift fr artisanal produc.n to"
    " mechanized manufacture, precipitating urbanization, the rise of"
    " factory labor, and new cls dynamics; & innovations in pub health,"
    " and pol repr. The period's cul ramifications incl the spread of"
    " literacy and reorder modn soc. This is really o.est."
)


# Entry Point  #################################################################
if __name__ == "__main__":
    blueprint = PromptBlueprint.parse(BLUEPRINT_TEXT, disable_prune=True)

    print(gen_comment_banner_centered("provided query", 1))
    print(QUERY)

    print(gen_comment_banner_centered("abbr node content", 2))
    prompt = blueprint.generate_prompt(
        query="use an algo to calc the avg",
    )
    print(prompt)
