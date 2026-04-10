# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments

# FIXME update difficulty to print

# output keys  #################################################################
OUTPUT_META_KEY = "meta_content"


# constants  ###################################################################
USAGE_TIME_KEY = "time_to_generate"
USAGE_TOKEN_KEY = "total_tokens"

ROLE2PRINTABLE_NAME = {
    "art": "🎨Art Tutor",
    "barista": "☕️Barista",
    "changelog": "🔄Changelog Writer",
    "chat": "💬Chat",
    "coder": "🧬Kaye Peer Coder",
    "deutschlehrer": "🇩🇪Deutschlehrer",
    "editor": "✍️Editor",
    "librarian": "🏛️Librarian",
    "prompt": "🖊️Prompt Writer",
    "rapid": "⚡️Rapid",
    "secretary": "💼Secretary",
    "tarot": "🔮Tarot Reader",
}


# helpers  #####################################################################
def _generate_usage_line(usage):
    return "`{}`s\t`{}`t".format(usage[USAGE_TIME_KEY], usage[USAGE_TOKEN_KEY])


def _generate_llm_usage_line(llm, usage):
    return "*{}*\t{}".format(llm, _generate_usage_line(usage))


# Entry Point  #################################################################
def main(
    show_meta_content: bool,
    should_skip_sense: bool,
    current_role: str,
    current_difficulty: int,
    current_pls: str,
    sense_usage: dict,
    is_direct_response,
    task_usages: dict,
    merger_usage: dict,
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
    :type current_difficulty: int
    :param current_pls:
    :type current_pls: str
    :param sense_usage:
    :type sense_usage: dict
    :param is_direct_response:
    :type is_direct_response: bool
    :param task_usages:
    :type task_usages: dict
    :param merger_usage:
    :type merger_usage: dict
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
    lines.append(
        "Role:\t{}".format(
            ROLE2PRINTABLE_NAME[current_role]
            if current_role in ROLE2PRINTABLE_NAME
            else current_role
        )
    )
    lines.append("Difficulty:\t{}".format(current_difficulty))

    if current_role == "coder":
        lines.append("PLs:\t{}".format(current_pls))

    # task ---------------------------------------------------------------------
    if is_direct_response:
        ((llm, usage),) = task_usages.items()
        lines.append("Task:\t" + _generate_llm_usage_line(llm, usage))
    else:
        lines.append("Task:")
        for llm, usage in task_usages.items():
            lines.append(_generate_llm_usage_line(llm, usage))

        lines.append("Merger:\t" + _generate_usage_line(merger_usage))

    # final content form  ------------------------------------------------------
    meta_content = """

> [!TIP]
""" + "\n".join("> " + line for line in lines)

    return {OUTPUT_META_KEY: str(meta_content)}
