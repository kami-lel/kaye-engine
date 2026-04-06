# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments


# HACK rm this
# output keys  #################################################################
OUTPUT_LLM_KEY = "llm"


# Entry Point  #################################################################
def main(
    role: str,
    llm_override: str,
    llm_sensed: str,
    difficulty_override: float,
    difficulty_sensed: float,
    difficulty_thresholds: list[float],
):
    """
    decide which LLM (branch) for this round of conversation


    :param role:
    :type role: str
    :param llm_override:
    :type llm_override: str
    :param llm_sensed:
    :type llm_sensed: str
    :param difficulty_override:
    :type difficulty_override: float
    :param difficulty_sensed:
    :type difficulty_sensed: float
    :param difficulty_thresholds:
            difficulty thresholds given as environment variable
    :type difficulty_thresholds: list[float]
    :return: {"llm": LLM to use for this round of conversation}
    :rtype: dict{"llm": str}
    """
    if llm_override:
        llm = llm_override

    elif role == "coder":

        difficulty = (
            difficulty_sensed
            if (difficulty_override == -1)
            else difficulty_override
        )

        if difficulty < difficulty_thresholds[0]:
            llm = "rapid"
        elif difficulty < difficulty_thresholds[1]:
            llm = "chat"
        elif difficulty < difficulty_thresholds[2]:
            llm = "think"
        else:
            llm = "think-think"

    elif role == "barista":
        llm = "chat"

    elif role == "deutschlehrer":
        llm = "think"

    elif role == "tarot":
        llm = "chat"

    else:
        llm = llm_sensed

    return {OUTPUT_LLM_KEY: llm}
