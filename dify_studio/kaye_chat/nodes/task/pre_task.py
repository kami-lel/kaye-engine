# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments


import json

# Output Key ###################################################################
OUTPUT_BODY_KEY = "task_prompt_getter_body"
OUTPUT_LLMS_KEY = "llms"
OUTPUT_DIRECT_KEY = "is_direct_response"


# constants  ###################################################################
THRESHOLDS = [
    (0, ["gpt-4-nano"]),
    (10, ["gpt-5-nano"]),
    (30, ["claude-sonnet-4"]),
    (60, ["claude-sonnet-4", "gpt-5-mini"]),
    (80, ["claude-opus-4", "gpt-5"]),
    (90, ["claude-opus-4", "gpt-5", "gemini-3-pro"]),
]
# (lower bounds, LLMs to use)


# Entry Point  #################################################################
def main(
    query: str,
    current_role: str,
    current_difficulty: float,
    current_pls: str,
):
    """
    create a json-typed GET body for task prompt getter


    :param query:
    :type query: str
    :param current_role:
    :type current_role: str
    :param current_pls:
    :type current_pls: str
    :param difficulty:
    :type difficulty: int
    :return: {
        "task_prompt_getter_body":  body sent to /task
        "llms":                     LLMs to use during tasks
        "is_direct_response":       whether use direct response mode during task
    }

    :rtype: dict{
        "task_prompt_getter_body":  str,
        "llms":                     list[str],
        "is_direct_response":       bool,
    }
    """
    # gen body  ----------------------------------------------------------------
    # used for Task Prompt Getter node

    body = {
        "query": query,
        "role": current_role,
        "programming_languages": current_pls,
    }
    body_json_dumps = json.dumps(body)

    # gen LLMs  ----------------------------------------------------------------
    llms = THRESHOLDS[0][1]
    for threshold, value in THRESHOLDS:
        if current_difficulty >= threshold:
            llms = value

    # is direct  ---------------------------------------------------------------
    is_direct_response = len(llms) == 1

    # Output Variables  --------------------------------------------------------
    return {
        OUTPUT_BODY_KEY: str(body_json_dumps),
        OUTPUT_LLMS_KEY: llms,
        OUTPUT_DIRECT_KEY: bool(is_direct_response),
    }
