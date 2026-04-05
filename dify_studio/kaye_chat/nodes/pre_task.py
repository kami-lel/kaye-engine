# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments


import json

# Output Key ###################################################################
OUTPUT_BODY_KEY = "body"
OUTPUT_LLMS_KEY = "llms"
OUTPUT_DIRECT_KEY = "is_direct_response"


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
    :rtype:
    TODO write docstring
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
    # TODO

    return {
        OUTPUT_BODY_KEY: body_json_dumps,
        OUTPUT_LLMS_KEY: None,
        OUTPUT_DIRECT_KEY: None,
    }
