# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_ROLE_KEY = "role"
OUTPUT_DIFF_KEY = "difficulty"


# Entry Point  #################################################################
def main(
    role_override: str,
    difficulty_override: float,
    current_role: str,
):
    # role  --------------------------------------------------------------------
    role = role_override or current_role or ""

    # difficulty   -------------------------------------------------------------
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

    return {OUTPUT_DIFF_KEY: diff}
