# pylint: disable=missing-module-docstring

import json

# Output Keys  #################################################################

OUTPUT_SKIP_KEY = "should_skip_sense"
OUTPUT_ROLE_KEY = "role"
OUTPUT_DIFF_KEY = "difficulty"
OUTPUT_SENSE_BODY_KEY = "sense_prompt_getter_body"

# constants  ###################################################################

# roles w/ static difficulty associated with it, thus should skip sense
STATIC_DIFFICULTY_ROLES = {
    "barista": 0.3,
    "deutschlehrer": 0.4,
    "tarot": 0.5,
}


# Body Key  ####################################################################
BODY_ROLE_KEY = "pre_sense_role"
BODY_DIFF_KEY = "difficulty_override"


# Entry Point  #################################################################
def main(
    role_override: str,
    difficulty_override: float,
    current_role: str,
):
    # decide role  -------------------------------------------------------------
    # role_override take priority
    # empty indicates sense node to decide it during 1st round
    role = role_override or current_role or ""

    # decide skip & diff  ------------------------------------------------------
    skip = False
    diff = 0.0

    if role in STATIC_DIFFICULTY_ROLES:
        skip = True
        diff = STATIC_DIFFICULTY_ROLES[role]

    elif role:
        skip = difficulty_override != 0
        diff = difficulty_override

    # body  --------------------------------------------------------------------
    if skip:
        body = ""
    else:
        body = json.dumps(
            {BODY_ROLE_KEY: role, BODY_DIFF_KEY: difficulty_override}
        )

    # Output Variables  --------------------------------------------------------
    return {
        OUTPUT_SKIP_KEY: skip,
        OUTPUT_ROLE_KEY: role,
        OUTPUT_DIFF_KEY: diff,
        OUTPUT_SENSE_BODY_KEY: body,
    }
