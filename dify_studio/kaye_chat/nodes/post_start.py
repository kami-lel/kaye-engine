# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_ROLE_KEY = "role"


# Entry Point  #################################################################


def main(
    role_override: str,
    current_role: str,
):
    # decide role  =============================================================
    role = current_role or role_override or ""

    return {OUTPUT_ROLE_KEY: role}
