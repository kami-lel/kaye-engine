# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_ROLE_KEY = "role"


# Entry Point  #################################################################


def main(role_override: str, llm_override: str, difficulty_override: float, current_role: str):
    # decide role  =============================================================
    role = current_role or role_override or ""
    # TODO

    return {OUTPUT_ROLE_KEY: role}
