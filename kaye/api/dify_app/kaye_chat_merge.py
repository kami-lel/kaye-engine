"""
define endpoint behavior of: /kaye/dify-app/ky/merge
"""

# pylint: disable=missing-function-docstring

from kaye.prompt import PromptBlueprint

# constant  ####################################################################

MERGE_PROMPT_BLUEPRINT = """ ○
[x] ├── Kaye Chat
[x] │   └── merge
"""


# Entry Point  #################################################################
def kaye_chat_merge():
    blueprint = PromptBlueprint.parse(MERGE_PROMPT_BLUEPRINT)

    # create concrete prompt  --------------------------------------------------
    return blueprint.generate_prompt()
