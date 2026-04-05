# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments


import json

# Output Key ###################################################################
OUTPUT_BODY_KEY = "body"
OUTPUT_LLMS_KEY = "llms"
OUTPUT_DIRECT_KEY = "is_direct_response"


# constants  ###################################################################
THRESHOLDS = [
    (0.0, ["gpt-5-nano"]),
    (0.2, ["claude-sonnet-4.6"]),
    (0.6, ["claude-sonnet-4.6", "gpt-5-mini"]),
    (0.9, ["claude-opus-4.6", "gpt-5"]),
]
# lower bounds: LLMs to use


# Entry Point  #################################################################
def main(
    query: str,
    current_role: str,
    current_pls: str,
    difficulty: float,
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
    :type difficulty: float
    :return:
    :rtype: dict{"body": str, "llms": list[str], "is_direct_response": bool}
    """
    # gen body  ================================================================
    # used for Task Prompt Getter node

    body = {
        "query": query,
        "role": current_role,
        "programming_languages": current_pls,
    }
    body_json_dumps = json.dumps(body)

    # gen LLMs  ================================================================
    llms = THRESHOLDS[0][1]
    for threshold, value in THRESHOLDS:
        if difficulty >= threshold:
            llms = value

    # is direct  ===============================================================
    is_direct_response = len(llms) == 1

    # returns  =================================================================
    return {
        OUTPUT_BODY_KEY: body_json_dumps,
        OUTPUT_LLMS_KEY: llms,
        OUTPUT_DIRECT_KEY: is_direct_response,
    }
