import json

# constants  ###################################################################
BODY_PROMPT_KEY = "prompt"
BODY_FLAGS_KEY = "flags"
OUTPUT_PROMPT_KEY = "task_prompt"
OUTPUT_PROMPT_FLAGS_KEY = "task_prompt_flags"


# entry point  #################################################################
def main(response_body: str):
    try:
        body_dict = json.loads(response_body)
        prompt = body_dict[BODY_PROMPT_KEY]
        flags = body_dict[BODY_FLAGS_KEY]
        return {OUTPUT_PROMPT_KEY: prompt, OUTPUT_PROMPT_FLAGS_KEY: flags}

    except json.JSONDecodeError as err:
        raise ValueError("fail to decode response_body as JSON") from err
