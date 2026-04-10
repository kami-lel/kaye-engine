# pylint: disable=missing-module-docstring


# Output Keys  #################################################################

OUTPUT_SKIP_KEY = "should_skip_sense"
OUTPUT_ROLE_KEY = "role"
OUTPUT_DIFF_KEY = "difficulty"

# constants  ###################################################################

# roles w/ static difficulty associated with it, thus should skip sense
STATIC_DIFFICULTY_ROLES = {
    "art": 52,
    "barista": 40,
    "changelog": 35,
    "deutschlehrer": 55,
    "editor": 47,
    "prompt": 85,
    "rapid": 1,
    "tarot": 46,
}


# Body Key  ####################################################################
BODY_ROLE_KEY = "pre_sense_role"
BODY_DIFF_KEY = "difficulty_override"


# Entry Point  #################################################################
def main(
    role_override: str,
    difficulty_override: int,
    current_role: str,
):
    """
    :param role_override:
    :type role_override: str
    :param difficulty_override:
    :type difficulty_override: int
    :param current_role:
    :type current_role: str
    :return: dict{
        "should_skip_sense":        whether should skip sense node in this round
        "role":                     current round role (so far)
        "difficulty":               current round difficulty (so far)
    }
    :rtype: dict{
        "should_skip_sense":        bool
        "role":                     str
        "difficulty":               int
    }
    """
    # decide role  -------------------------------------------------------------
    # role_override take priority
    # empty indicates sense node to decide it during 1st round
    role = role_override or current_role or ""

    # decide skip & diff  ------------------------------------------------------
    skip = False
    diff = 0

    if role in STATIC_DIFFICULTY_ROLES:
        skip = True
        diff = STATIC_DIFFICULTY_ROLES[role]

    elif role == "coder":
        pass  # coder never skip

    elif role:
        skip = difficulty_override != 0

    # override difficulty from input
    if difficulty_override != 0:
        diff = difficulty_override

    # Output Variables  --------------------------------------------------------
    return {
        OUTPUT_SKIP_KEY: bool(skip),
        OUTPUT_ROLE_KEY: str(role),
        OUTPUT_DIFF_KEY: int(diff),
    }
