# pylint: disable=missing-module-docstring

# HACK HACK rm

# Output Keys  #################################################################

OUTPUT_SKIP_KEY = "should_skip_sense"


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
    :param role_override:
    :type role_override: str
    :param difficulty_override:
    :type difficulty_override: float
    :param current_role:
    :type current_role: str
    :return: {"should_skip_sense": whether should skip sense node in current round}
    :rtype: dict{"should_skip_sense": bool}
    """

    role = role_override or current_role or ""

    if role in STATIC_DIFFICULTY_ROLES:  # skip b/c roles
        skip = True

    elif role:
        skip = difficulty_override != 0

    else:  # unknown role
        skip = False

    # output vars  =============================================================
    return {OUTPUT_SKIP_KEY: skip}
