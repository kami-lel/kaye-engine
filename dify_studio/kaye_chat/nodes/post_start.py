# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_ROLE_KEY = "role"
OUTPUT_SKIP_KEY = "skip_pre_sense"


# Entry Point  #################################################################


def main(
    role_override: str,
    llm_override: str,
    difficulty_override: float,
    current_role: str,
):
    # decide role  =============================================================
    role = current_role or role_override or ""

    # decide if skip pre-sense  ================================================
    skip_pre_sense = (
        role == "peer_coder" and (difficulty_override or llm_override)
    ) or (role and llm_override)

    return {OUTPUT_ROLE_KEY: role, OUTPUT_SKIP_KEY: bool(skip_pre_sense)}
