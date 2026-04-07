# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments


# output keys  #################################################################
OUTPUT_ROLE_KEY = "role"
OUTPUT_DIFF_KEY = "difficulty"
OUTPUT_PLS_KEY = "combined_pls"


# constant  ####################################################################
SPLITTER = ","


# Entry Point  #################################################################
def main(
    sensed_role: str,
    sensed_difficulty: int,
    sensed_pls: str,
    current_role: str,
    difficulty_override: int,
    current_pls: str,
):
    """
    collect & organize information from sense code


    :param sensed_role:
    :type sensed_role: str
    :param sensed_difficulty:
    :type sensed_difficulty: int
    :param sensed_pls:
    :type sensed_pls: str
    :param current_role:
    :type current_role: str
    :param difficulty_override:
    :type difficulty_override: int
    :param current_pls:
    :type current_pls: str
    :return: {
        "role":         final/post-sense role for current round
        "difficulty":   final/post-sense difficulty for current round
        "combined_pls": combined PLs
    }
    :rtype: dict{"role": str, "difficulty": int, "combined_pls": str}
    """
    # role  --------------------------------------------------------------------
    # role default to chat
    role = current_role or sensed_role or "chat"

    # difficulty  --------------------------------------------------------------
    difficulty = difficulty_override or sensed_difficulty or 0

    # pls  ---------------------------------------------------------------------
    combined_set = set(current_pls.split(SPLITTER)) | set(
        sensed_pls.split(SPLITTER)
    )
    combined_pls = SPLITTER.join(filter(bool, combined_set))

    return {
        OUTPUT_ROLE_KEY: str(role),
        OUTPUT_DIFF_KEY: int(difficulty),
        OUTPUT_PLS_KEY: str(combined_pls),
    }
