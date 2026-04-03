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
    """
    collect & organize information from sense code


    :param current_pls:
    :type current_pls: str
    :param sensed_pls:
    :type sensed_pls: dict
    :param current_role:
    :type current_role: str
    :param sensed_role: role saved in conversation variable
    :type sensed_role: str
    :return: {
            "combined_pls": combined PLs saved in conversation variable
            (PLs from last rounds of this conversations)
            with new PLs from sense node in this round
            "role": role to used for this round of conversation}
    :rtype: dict{"combined_pls": str "role": str}
    """
    # TODO update
    # pls  ---------------------------------------------------------------------
    combined_set = set(current_pls.split(SPLITTER)) | set(
        sensed_pls.split(SPLITTER)
    )
    combined_pls = SPLITTER.join(filter(bool, combined_set))

    # role  --------------------------------------------------------------------
    role = current_role or sensed_role or "chat"

    return {OUTPUT_COMBINED_KEY: combined_pls, OUTPUT_ROLE_KEY: role}
