# pylint: disable=missing-module-docstring

import json

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
            "should_sense_role": bool,
            "sense_prompt_getter_body": str
            }
    """

    # decide role  -------------------------------------------------------------
    # role_override take priority
    # empty indicates sense node to decide it during 1st round
    role = role_override or current_role or ""

    # skip sense logic  --------------------------------------------------------

    diff_provided = difficulty_override != 0

    # default values
    sense_role = False
    sense_diff = "default"

    if role in STATIC_DIFFICULTY_ROLES:  # skip b/c roles
        skip = True

    elif role:
        skip = diff_provided

        if role == "coder":
            sense_diff = "coder"

    else:  # unknown role
        skip = False
        sense_role = True
        sense_diff = "default"

    # FIXME FIXME use good name
    body = json.dumps(
        {"has_role_prompt": sense_role, "difficulty_role": sense_diff}
    )

    return {
        "pre_sense_role": role,
        "should_skip_sense": skip,
        "sense_prompt_getter_body": body,
    }
