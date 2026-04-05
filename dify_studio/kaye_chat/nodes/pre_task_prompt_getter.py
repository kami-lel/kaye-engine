# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments


import json

# output keys  #################################################################
OUTPUT_BODY_KEY = "body"


# Entry Point  #################################################################
def main(query: str, current_role: str, current_pls: str):
    """
    create a json-typed GET body for task prompt getter


    :param query:
    :type query: str
    :param current_role:
    :type current_role: str
    :param current_pls:
    :type current_pls: str
    :return: {"body": generated JSON GET body}
    :rtype: dict{"body": str}
    """

    body = {
        "query": query,
        "role": current_role,
        "programming_languages": current_pls,
    }
    body_json_dumps = json.dumps(body)

    return {OUTPUT_BODY_KEY: body_json_dumps}
