# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_COMBINED_KEY = "combined_pls"
OUTPUT_ROLE_KEY = "role"


# constant  ####################################################################
SPLITTER = ","


# Entry Point  #################################################################
def main(
    current_pls: str,
    sensed_pls: dict,
    current_role: str,
    sensed_role: dict,
):
    # pls  ---------------------------------------------------------------------
    combined_set = set(current_pls.split(SPLITTER)) | set(
        sensed_pls.split(SPLITTER)
    )
    combined_pls = SPLITTER.join(combined_set)

    # role  --------------------------------------------------------------------
    role = current_role or sensed_role or "chat"

    return {OUTPUT_COMBINED_KEY: combined_pls, OUTPUT_ROLE_KEY: role}
