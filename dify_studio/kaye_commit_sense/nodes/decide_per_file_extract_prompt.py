# pylint: disable=missing-module-docstring

# output keys  #################################################################
OUTPUT_PROMPT_KEY = "extract_prompt"


# constants  ###################################################################
LONG_SHORT_THRESHOLD = 100


# entry point  #################################################################
def main(
    item: str,
    prompt_per_file_extract_long: str,
    prompt_per_file_extract_short: str,
):
    """
    count number of lines, and decide to use either long/short prompts


    :param item:
    :type item: str
    :param prompt_per_file_extract_long:
    :type prompt_per_file_extract_long: str
    :param prompt_per_file_extract_short:
    :type prompt_per_file_extract_short: str
    :return: {"extract_prompt": prompt to use}
    :rtype: dict{"extract_prompt": str}
    """
    newline_cnt = item.count("\n")
    is_long = newline_cnt > LONG_SHORT_THRESHOLD

    return {
        OUTPUT_PROMPT_KEY: (
            prompt_per_file_extract_long
            if is_long
            else prompt_per_file_extract_short
        )
    }
