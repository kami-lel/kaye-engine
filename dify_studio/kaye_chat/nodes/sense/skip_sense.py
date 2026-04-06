# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_META_KEY = "difficulty"

# constants  ###################################################################


# Entry Point  #################################################################
def main(
    role: str,
    difficulty_override: float,
):
    if difficulty_override:
        diff = difficulty_override

    else:

        if role == "barista":
            diff = 0.2
        elif role == "deutschlehrer":
            diff = 0.35
        elif role == "tarot":
            diff = 0.3
        else:
            diff = 0.01

    return {OUTPUT_META_KEY: diff}
