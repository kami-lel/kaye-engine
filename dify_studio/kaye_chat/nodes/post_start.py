# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_ROLE_KEY = "pre_sense_role"
OUTPUT_SKIP_KEY = "should_skip_sense"


# constants  ###################################################################

# roles w/ static difficulty associated with it, thus should skip sense
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
    # TODO write docstring

    # decide role  -------------------------------------------------------------
    # pre-sense role should be empty during 1st round
    # and not provided by role_override
    role = role_override or current_role or ""

    # decide skip  -------------------------------------------------------------
    if role in SKIP_SENSE_ROLES:  # skip b/c roles
        skip = True

    elif role:
        # both both & LLM are provided
        skip = bool(difficulty_override)

    else:
        skip = False

    return {OUTPUT_ROLE_KEY: role, OUTPUT_SKIP_KEY: skip}
