# pylint: disable=missing-module-docstring

import json

# Output Keys  #################################################################

OUTPUT_BODY_KEY = "getter_request_body"
OUTPUT_QUERY_KEY = "filtered_query"


# Body Key  ####################################################################
BODY_ROLE_KEY = "pre_sense_role"
BODY_DIFF_KEY = "difficulty_override"


# constants  ###################################################################
QUERY_LINE_LIMIT = 100


# Entry Point  #################################################################
def main(current_role: str, difficulty_override: int, query: str):
    # body  --------------------------------------------------------------------
    getter_body = json.dumps(
        {BODY_ROLE_KEY: current_role, BODY_DIFF_KEY: difficulty_override}
    )

    # filter query  ------------------------------------------------------------
    # split as lines and remove empty lines
    lines = [line for line in query.splitlines if line.strip()]

    if len(lines) > QUERY_LINE_LIMIT:
        n = QUERY_LINE_LIMIT / 2
        head = lines[:n]
        tail = lines[-n:]
        filtered_query = "\n".join(head + tail)

    else:  # short, no no op
        filtered_query = query

    return {
        OUTPUT_BODY_KEY: str(getter_body),
        OUTPUT_QUERY_KEY: str(filtered_query),
    }
