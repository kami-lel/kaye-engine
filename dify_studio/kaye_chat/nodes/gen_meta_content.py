# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments


# output keys  #################################################################
OUTPUT_META_KEY = "meta_content"


# constants  ###################################################################
USAGE_TIME_KEY = "time_to_generate"
USAGE_TOKEN_KEY = "total_tokens"


# helpers  #####################################################################
def _generate_usage_line(usage):
    return "{}s\t{}t".format(usage[USAGE_TIME_KEY], usage[USAGE_TOKEN_KEY])


# Entry Point  #################################################################


def main(
    show_meta_content: bool,
    should_skip_sense: bool,
    current_role: str,
    current_difficulty: float,
    current_pls: str,
    sense_usage: dict,
    task_usages: dict,
):
    """
    generate meta content for debug


    :param show_meta_content:
    :type show_meta_content: bool
    :param should_skip_sense:
    :type should_skip_sense: bool
    :param current_role:
    :type current_role: str
    :param current_difficulty:
    :type current_difficulty: float
    :param current_pls:
    :type current_pls: str
    :param sense_usage:
    :type sense_usage: dict
    :param task_usages:
    :type task_usages: dict
    :return: {"meta_content": meta content for debug}
    :rtype: dict{"meta_content": str}
    """
    if not show_meta_content:
        return {OUTPUT_META_KEY: ""}

    lines = []

    # sense-related  -----------------------------------------------------------
    if not should_skip_sense:
        lines.append("Sensed:\t" + _generate_usage_line(sense_usage))

    # task parameters  ---------------------------------------------------------
    lines.append("Role:\t{}".format(current_role))
    lines.append("Difficulty:\t{}".format(current_difficulty))

    if current_role == "coder":
        lines.append("PLs:\t{}".format(current_pls))

    # task ---------------------------------------------------------------------
    lines.append("Task:")
    for llm, usage in task_usages.items():
        lines.append("{}:\t{}".format(llm, _generate_usage_line(usage)))

    # final content form  ------------------------------------------------------
    meta_content = """

> [!TIP]
""" + "\n".join("> " + line for line in lines)

    return {OUTPUT_META_KEY: meta_content}
