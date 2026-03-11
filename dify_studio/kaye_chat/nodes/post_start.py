# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_ROLE_KEY = "role"
OUTPUT_SKIP_KEY = "skip_sense"


# helpers  #####################################################################
def should_skip_sense(role, difficulty_override, llm_override):
    # Bug dont skip for coder, b/c still need to extract PLs during sensing
    # TODO add for barista
    skip = (role == "coder" and (difficulty_override or llm_override)) or (
        role and llm_override
    )
    return bool(skip)


# Entry Point  #################################################################
def main(
    role_override: str,
    llm_override: str,
    difficulty_override: float,
    current_role: str,
):
    """
    prepare parameters for **this round**
    based on variables provided by *User Input Fields*


    :param role_override:
    :type role_override: str
    :param llm_override:
    :type llm_override: str
    :param difficulty_override:
    :type difficulty_override: float
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

    skip_sense = should_skip_sense(role, difficulty_override, llm_override)

    return {OUTPUT_ROLE_KEY: role, OUTPUT_SKIP_KEY: skip_sense}
