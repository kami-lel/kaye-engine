# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_LLM_KEY = "llm"


# Entry Point  #################################################################
def main(
    llm_override: str,
    llm_sensed: dict,
    difficulty_override: float,
    difficulty_sensed: dict,
    role: str,
):
    # TODO
    llm = ""
    return {OUTPUT_LLM_KEY: llm}
