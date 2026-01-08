from kaye.gen_prompt import PromptBlueprint, load_embedded_prompt_corpus

PROMPT_BLUEPRINT = """○
[ ] └── Role
[ ]     └── Kaye Cash Tracker
[x]         └── Extract Info
"""


def call_kaye_cash_tracker():
    # pylint: disable=missing-function-docstring

    blueprint = PromptBlueprint(
        load_embedded_prompt_corpus(),
        PROMPT_BLUEPRINT,
    )

    return str(blueprint)
