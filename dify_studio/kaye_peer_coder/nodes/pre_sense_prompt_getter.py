BLUEPRINT = """ ○
[x] ├── Role
[x] │   └── Kaye Peer Coder
[x] │       └── pre-sense
[x] └── Abbreviations
[x]     └── Programming Languages
"""


# constants  ###################################################################
PROMPT_KEY_IN_CACHE = "pre_sense_prompt"
OUTPUT_PROMPT_KEY = "presense_prompt"
OUTPUT_CACHES_KEY = "updated_caches"


# entry point  #################################################################
def main(caches: dict):
    if PROMPT_KEY_IN_CACHE in caches:
        return {
            OUTPUT_PROMPT_KEY: caches[PROMPT_KEY_IN_CACHE],
            OUTPUT_CACHES_KEY: caches,
        }

    else:
        # get prompt from API  -------------------------------------------------
        # Todo use API
        presense_prompt = ""

        # update Conversation Variable caches
        caches[PROMPT_KEY_IN_CACHE] = presense_prompt
        return {
            OUTPUT_PROMPT_KEY: presense_prompt,
            OUTPUT_CACHES_KEY: caches,
        }
