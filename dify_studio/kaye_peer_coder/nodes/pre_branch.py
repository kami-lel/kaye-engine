"""
decide which branch/LLM to use depending on difficulty


:param difficulty:
:type difficulty: float
:param difficulty_thresholds:
:type difficulty_thresholds: list[float]
:return: { "llm": which LLM to be used }
:rtype: dict{ "llm": str }
"""

# output keys  #################################################################
OUTPUT_LLM_KEY = "llm"


# Entry Point  #################################################################
def main(
    difficulty: float,
    difficulty_thresholds: list[float],
):  # pylint: disable=missing-function-docstring
    # decide branch  -----------------------------------------------------------
    if difficulty < difficulty_thresholds[0]:
        llm = "LLM I"
    elif difficulty < difficulty_thresholds[1]:
        llm = "LLM II"
    else:
        llm = "LLM III"

    return {OUTPUT_LLM_KEY: llm}
