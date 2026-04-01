# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_ROLE_KEY = "pre_sense_role"
OUTPUT_SKIP_KEY = "should_skip_sense"


# constants  ###################################################################

SKIP_SENSE_ROLES = [
    "barista",
    "deutschlehrer",
    "tarot",
]


# Entry Point  #################################################################
def main(
    role_override: str,
    difficulty_override: float,
    current_role: str,
):
    # BUG write codes
    # decide role  -------------------------------------------------------------
    role = role_override or current_role or ""

    # decide skip  -------------------------------------------------------------
    if role in SKIP_SENSE_ROLES:
        skip = True

    elif role:
        # both both & LLM are provided
        skip = bool(difficulty_override)

    else:
        skip = False

    return {OUTPUT_ROLE_KEY: role, OUTPUT_SKIP_KEY: skip}
