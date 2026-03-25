# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments


import json

# output keys  #################################################################
OUTPUT_BODY_KEY = "body"


# Entry Point  #################################################################
def main(query: str, role: str, programming_languages: str):
    """
    create a json-typed GET body for task prompt getter


    :param query:
    :type query: str
    :param role:
    :type role: str
    :param programming_languages:
    :type programming_languages: str
    :return: {"body": generated JSON GET body}
    :rtype: dict{"body": str}
    """

    body = {
        "query": query,
        "role": role,
        "programming_languages": programming_languages,
    }
    body_json_dumps = json.dumps(body)

    return {OUTPUT_BODY_KEY: body_json_dumps}
