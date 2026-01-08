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


PRESENSE_PROMPT_KEY = "presense_prompt"


def main(presense_prompt_cache: str):
    if presense_prompt_cache:  # not empty, already performed
        return {PRESENSE_PROMPT_KEY: presense_prompt_cache}

    else:
        # get prompt from API  -------------------------------------------------
        # Todo use API
        presense_prompt = ""
        return {PRESENSE_PROMPT_KEY: presense_prompt}
