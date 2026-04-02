# pylint: disable=missing-module-docstring


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
            }
    :rtype: dict{"pre_sense_role": str, "should_skip_sense": bool}
    """

    # decide role  -------------------------------------------------------------
    # role_override take priority
    # empty indicates sense node to decide it during 1st round
    role = role_override or current_role or ""

    # TODO determine sense

    # decide skip  -------------------------------------------------------------
    if role in SKIP_SENSE_ROLES:  # skip b/c roles
        skip = True
        sense_role = True
        sense_diff = "default"

    elif role:
        # if difficulty is provided, skip sense given role
        skip = difficulty_override != 0
        sense_role = True
        sense_diff = "default"

    else:
        # both role and difficulty role are unknown, thus require sense
        skip = False
        sense_role = True
        sense_diff = "default"

    return {
        "pre_sense_role": role,
        "should_skip_sense": skip,
        "should_sense_role": sense_role,
        "sense_difficulty_select": sense_diff,
    }
