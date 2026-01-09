# pylint: disable=missing-module-docstring


import json

# constants  ###################################################################
BODY_PROMPT_KEY = "prompt"
BODY_FLAGS_KEY = "flags"
OUTPUT_PROMPT_KEY = "task_prompt"
OUTPUT_PROMPT_FLAGS_KEY = "task_prompt_flags"


# entry point  #################################################################
def main(response_body: str):
    """
    parse response body from Kaye API into prompt and prompts' flags for caching


    :param response_body: response body (typed `application/json`)
            returned from Kaye API
    :type response_body: str
    :raises ValueError: _description_
    :return: {"task_prompt": ~, "task_prompt_flags": ~}
    :rtype: dict{"task_prompt": str, "task_prompt_flags": int}
    """
    try:
        body_dict = json.loads(response_body)
        prompt = body_dict[BODY_PROMPT_KEY]
        flags = body_dict[BODY_FLAGS_KEY]
        return {OUTPUT_PROMPT_KEY: prompt, OUTPUT_PROMPT_FLAGS_KEY: flags}

    except json.JSONDecodeError as err:
        raise ValueError("fail to decode response_body as JSON") from err
