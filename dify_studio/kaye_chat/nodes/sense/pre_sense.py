# pylint: disable=missing-module-docstring


# Output Keys  #################################################################

OUTPUT_BODY_KEY = "getter_request_body"
OUTPUT_QUERY_KEY = "filtered_query"


# Entry Point  #################################################################
def main(current_role: str, difficulty_override: float, query: str):
    getter_body = ""

    filtered_query = ""
    # TODO ky: smart sense, take only part of the user's input as sense message:
    # eg by taking first n lines + last n lines
    # eg by removing all codes block out

    return {OUTPUT_BODY_KEY: getter_body, OUTPUT_QUERY_KEY: filtered_query}
