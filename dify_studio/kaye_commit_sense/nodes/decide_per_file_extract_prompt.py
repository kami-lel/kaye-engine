"""
count number of lines, and decide to use either long/short prompts

TODO params
"""

# constants  ###################################################################
OUTPUT_PROMPT_KEY = "extract_prompt"
LONG_SHORT_THRESHOLD = 100


# entry point  #################################################################
def main(
    item: str,
    prompt_per_file_extract_long: str,
    prompt_per_file_extract_short: str,
):  # pylint: disable=missing-function-docstring
    newline_cnt = item.count("\n")
    is_long = newline_cnt > LONG_SHORT_THRESHOLD

    return {
        OUTPUT_PROMPT_KEY: (
            prompt_per_file_extract_long
            if is_long
            else prompt_per_file_extract_short
        )
    }
