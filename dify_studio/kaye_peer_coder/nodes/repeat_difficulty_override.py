"""
repeat the difficulty override (for the aggregator)


:param difficulty_override: difficult override value given from user input
:type difficulty_override: float
:return: {"difficulty": difficulty value}
:rtype: dict{"difficulty": float}
"""

# output keys  #################################################################
OUTPUT_DIFFICULT_KEY = "difficulty"


# Entry Point  #################################################################


def main(
    difficulty_override: float,
):  # pylint: disable=missing-function-docstring
    return {OUTPUT_DIFFICULT_KEY: difficulty_override}
