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
    TODO

    :param current_pls: _description_
    :type current_pls: str
    :param sensed_pls: _description_
    :type sensed_pls: dict
    :param current_role: _description_
    :type current_role: str
    :param sensed_role: _description_
    :type sensed_role: dict
    :return: _description_
    :rtype: _type_
    """
    # pls  ---------------------------------------------------------------------
    combined_set = set(current_pls.split(SPLITTER)) | set(
        sensed_pls.split(SPLITTER)
    )
    combined_pls = SPLITTER.join(filter(bool, combined_set))

    # role  --------------------------------------------------------------------
    role = current_role or sensed_role or "chat"

    return {OUTPUT_COMBINED_KEY: combined_pls, OUTPUT_ROLE_KEY: role}
