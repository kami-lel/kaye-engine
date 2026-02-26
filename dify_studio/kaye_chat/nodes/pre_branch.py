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

    if role == "peer_coder":
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
