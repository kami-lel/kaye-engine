# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_ROLE_KEY = "role"
OUTPUT_SKIP_KEY = "skip_sense"


# constants  ###################################################################

SKIP_SENSE_ROLES = [
    "barista",
    "deutschlehrer",
    "tarot",
]


# helpers  #####################################################################
def should_skip_sense(role, llm_override):
    """
    decide whether should skip sense node for this round of conversation
    based on combination of difficulty & LLM overrides given


    :param role:
    :type role: str
    :param llm_override:
    :type llm_override: str
    :return: whether should skip sense node
    :rtype: bool
    """
    # these roles should skip sense node
    # for having a fixed LLM associated
    if role in SKIP_SENSE_ROLES:
        return True

    # Bug coder should skip if provided LLM or difficulty
    elif role:
        # both both & LLM are provided
        return bool(llm_override)

    return False


# Entry Point  #################################################################
def main(
    role_override: str,
    llm_override: str,
    current_role: str,
):
    """
    prepare parameters for **this round**
    based on variables provided by *User Input Fields*


    :param role_override:
    :type role_override: str
    :param llm_override:
    :type llm_override: str
    :param current_role: role saved in conversation variable,
            often decided on 1st round of conversation
    :type current_role: str
    :return: {
            "role": role to used for this round of conversation,
            "skip_sense": whether skip sense node in this round}
    :rtype: dict{"role": str, "skip_sense": bool}
    """
    # decide role  =============================================================
    role = role_override or current_role or ""

    skip_sense = should_skip_sense(role, llm_override)

    return {OUTPUT_ROLE_KEY: role, OUTPUT_SKIP_KEY: skip_sense}
