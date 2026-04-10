# pylint: disable=missing-module-docstring

import json

# Output Keys  #################################################################

OUTPUT_BODY_KEY = "getter_request_body"
OUTPUT_QUERY_KEY = "filtered_query"


# Body Key  ####################################################################
BODY_ROLE_KEY = "pre_sense_role"
BODY_DIFF_KEY = "difficulty_override"


# Entry Point  #################################################################
def main(current_role: str, difficulty_override: float, query: str):
    # body  --------------------------------------------------------------------
    getter_body = json.dumps(
        {BODY_ROLE_KEY: current_role, BODY_DIFF_KEY: difficulty_override}
    )

    # filter query  ------------------------------------------------------------

    filtered_query = ""
    # TODO ky: smart sense, take only part of the user's input as sense message:
    # eg by taking first n lines + last n lines
    # eg by removing all codes block out

    return {OUTPUT_BODY_KEY: getter_body, OUTPUT_QUERY_KEY: filtered_query}
