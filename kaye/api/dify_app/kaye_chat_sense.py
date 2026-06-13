"""
kaye_chat_sense.py

define endpoint behavior of: /kaye/dify-app/ky/sense
"""

# pylint: disable=missing-function-docstring


from flask import request


from kaye.prompt import PromptBlueprint

# constant  ####################################################################
SENSE_PROMPT_BLUEPRINT = """ ○
[x] ├── Kaye Chat
[x] │   └── sense
[ ] │       ├── sense role
[ ] │       ├── sense difficulty
[ ] │       ├── programming_languages
[ ] │       │── sense coder difficulty
[ ] │       ├── empty role
[ ] │       ├── zero difficulty
[ ] │       └── empty programming_languages
[ ] └── (Programming Languages Code)
"""


# Entry Point  #################################################################
def kaye_chat_sense():
    body = request.get_json(silent=True) or {}

    role = body.get("pre_sense_role") or ""
    diff = body.get("difficulty_override") or 0

    blueprint = PromptBlueprint.parse(
        SENSE_PROMPT_BLUEPRINT, disable_prune=True
    )
    sense_node = blueprint.corpus["Kaye Chat"]["sense"]

    # on role  -----------------------------------------------------------------
    if role == "coder":
        blueprint.checkmark(sense_node["programming_languages"])
        blueprint.checkmark(sense_node["empty role"])
        blueprint.checkmark("(Programming Languages Code)")

        if diff == 0:
            blueprint.checkmark(sense_node["sense coder difficulty"])
        else:
            blueprint.checkmark(sense_node["zero difficulty"])

    elif role:  # other role
        # sense for difficult only
        blueprint.checkmark(sense_node["sense difficulty"])
        blueprint.checkmark(sense_node["empty role"])
        blueprint.checkmark(sense_node["empty programming_languages"])

    elif diff != 0:  # default role w/ provided difficulty override
        # sense for role only
        blueprint.checkmark(sense_node["sense role"])
        blueprint.checkmark(sense_node["zero difficulty"])
        blueprint.checkmark(sense_node["empty programming_languages"])

    else:  # default role w/o difficulty override
        # sense for role and difficulty
        blueprint.checkmark(sense_node["sense role"])
        blueprint.checkmark(sense_node["sense difficulty"])
        blueprint.checkmark(sense_node["empty programming_languages"])

    # create concrete prompt  --------------------------------------------------
    return blueprint.generate_prompt()
