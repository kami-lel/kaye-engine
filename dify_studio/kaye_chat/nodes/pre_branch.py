# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_LLM_KEY = "llm"


# Entry Point  #################################################################
def main(
    role: str,
    llm_override: str,
    llm_sensed: dict,
    difficulty_override: float,
    difficulty_sensed: dict,
    difficulty_thresholds: list[float],
):
    """
    TODO

    :param role: _description_
    :type role: str
    :param llm_override: _description_
    :type llm_override: str
    :param llm_sensed: _description_
    :type llm_sensed: dict
    :param difficulty_override: _description_
    :type difficulty_override: float
    :param difficulty_sensed: _description_
    :type difficulty_sensed: dict
    :param difficulty_thresholds: _description_
    :type difficulty_thresholds: list[float]
    :return: _description_
    :rtype: _type_
    """

    if role == "coder":
        difficulty = difficulty_override or difficulty_sensed
        if difficulty < difficulty_thresholds[0]:
            llm = "rapid"
        elif difficulty < difficulty_thresholds[1]:
            llm = "think"
        else:
            llm = "think-think"

    else:
        llm = llm_override or llm_sensed

    return {OUTPUT_LLM_KEY: llm}
