"""
decide which branch/LLM to use depending on difficulty


:param difficulty:
:type difficulty: int
:param difficulty_thresholds:
:type difficulty_thresholds: list[float]
:return: { "llm": 0~2, which LLM to be used }
:rtype: dict{ "llm": int }
"""

# output keys  #################################################################
OUTPUT_LLM_KEY = "llm"


# Entry Point  #################################################################
def main(
    difficulty: int,
    difficulty_thresholds: list[float],
):  # pylint: disable=missing-function-docstring
    # decide branch  -----------------------------------------------------------
    if difficulty < difficulty_thresholds[0]:
        llm = 0
    elif difficulty < difficulty_thresholds[1]:
        llm = 1
    else:
        llm = 2

    return {OUTPUT_LLM_KEY: llm}
