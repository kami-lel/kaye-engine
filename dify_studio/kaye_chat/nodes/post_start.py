# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_ROLE_KEY = "role"
OUTPUT_SKIP_KEY = "skip_sense"


# Entry Point  #################################################################
def main(
    role_override: str,
    llm_override: str,
    difficulty_override: float,
    current_role: str,
):
    # decide role  =============================================================
    role = role_override or current_role or ""

    # decide if skip sense  ====================================================
    skip_pre_sense = (
        role == "coder" and (difficulty_override or llm_override)
    ) or (role and llm_override)
    # bug dont skip for coder, b/c still need to extract PLs during sensing

    return {OUTPUT_ROLE_KEY: role, OUTPUT_SKIP_KEY: bool(skip_pre_sense)}
