"""
get `pre-sense` node's prompts from Kaye's Flask API
"""

KEY_IN_PROMPTS_CACHE = "pre-sense"


BLUEPRINT = """ ○
[x] ├── Role
[x] │   └── Kaye Peer Coder
[x] │       └── pre-sense
[x] └── Abbreviations
[x]     └── Programming Languages
"""


def main(prompts_cache: dict):
    # prompt already in cache
    if KEY_IN_PROMPTS_CACHE in prompts_cache:
        system_message = prompts_cache[KEY_IN_PROMPTS_CACHE]

    else:
        # get prompt from API  -------------------------------------------------
        # Todo use API
        system_message = ""

        # update Conversation Variable
        prompts_cache[KEY_IN_PROMPTS_CACHE] = system_message

    return {"system_message": system_message, "prompts_cache": prompts_cache}
