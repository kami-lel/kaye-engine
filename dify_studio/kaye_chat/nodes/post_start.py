# pylint: disable=missing-module-docstring

import json

# Output Keys  #################################################################

OUTPUT_ROLE_KEY = "pre_sense_role"
OUTPUT_SKIP_KEY = "should_skip_sense"
OUTPUT_SENSE_BODY_KEY = "sense_prompt_getter_body"


# Body Key  ####################################################################
BODY_ROLE_KEY = "pre_sense_role"
BODY_DIFF_KEY = "difficulty_override"


# constants  ###################################################################

# roles w/ static difficulty associated with it, thus should skip sense
STATIC_DIFFICULTY_ROLES = [
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
    """
    parsing *User Input* nodes' settings
    directly after *Start* and before *Sense* node


    :param role_override:
    :type role_override: str
    :param difficulty_override:
    :type difficulty_override: float
    :param current_role:
    :type current_role: str
    :return: {"pre_sense_role": role for this conversation
            "should_skip_sense": whether should skip sense node in this round
            "sense_prompt_getter_body": body sent to ``/sense`` endpoint
            }
    :rtype: dict{"pre_sense_role": str,
            "should_skip_sense": bool,
            "sense_prompt_getter_body": str
            }
    """

    # decide role  -------------------------------------------------------------
    # role_override take priority
    # empty indicates sense node to decide it during 1st round
    role = role_override or current_role or ""

    # skip sense logic  --------------------------------------------------------

    if role in STATIC_DIFFICULTY_ROLES:  # skip b/c roles
        skip = True

    elif role:
        skip = difficulty_override != 0

    else:  # unknown role
        skip = False

    body = json.dumps({BODY_ROLE_KEY: role, BODY_DIFF_KEY: difficulty_override})

    return {
        OUTPUT_ROLE_KEY: role,
        OUTPUT_SKIP_KEY: skip,
        OUTPUT_SENSE_BODY_KEY: body,
    }
