# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments

# Bug s/X replied 2 meta content during 2nd round conversation

# output keys  #################################################################
OUTPUT_META_KEY = "meta_content"


# Entry Point  #################################################################
def main(
    show_meta_content: bool,
    role_override: str,
    role: str,
    llm_override: str,
    llm_used: str,
    difficulty_override: float,
    difficulty_sensed: float,
    skip_sense: bool,
    programming_languages: str,
    sense_usage: dict,
    task_usage: dict,
):
    """
    generate **meta content**, information for debugging and testing


    :param show_meta_content: whether to show meta content,
            set as User Input Field
    :type show_meta_content: bool
    :param role_override:
    :type role_override: str
    :param role:
    :type role: str
    :param llm_override:
    :type llm_override: str
    :param llm_used:
    :type llm_used: str
    :param difficulty_override:
    :type difficulty_override: float
    :param difficulty_sensed:
    :type difficulty_sensed: float
    :param skip_sense:
    :type skip_sense: bool
    :param programming_languages:
    :type programming_languages: str
    :param sense_usage: usage object for information of sense node
    :type sense_usage: dict
    :param task_usage: usage object for information of task node
    :type task_usage: dict
    """
    if not show_meta_content:
        return {OUTPUT_META_KEY: ""}

    lines = []

    # create role line
    if role_override:
        lines.append("Role (Override): {}".format(role_override))
    else:
        lines.append("Role: {}".format(role))

    # create llm line
    if llm_override:
        lines.append(
            "LLM (Override): {}".format(_llm2display_name(llm_override))
        )
    else:
        lines.append("LLM: {}".format(_llm2display_name(llm_used)))

    role_used = role_override or role
    if role_used == "coder":
        if difficulty_override == -1:
            lines.append("Difficulty: {}".format(difficulty_sensed))
        else:
            lines.append(
                "Difficulty (Override): {}".format(difficulty_override)
            )

        lines.append("PLs: {}".format(programming_languages))

    if not skip_sense:
        lines.append("Sense: {}s".format(sense_usage[USAGE_TIME_KEY]))

    lines.append("Task: {}s".format(task_usage[USAGE_TIME_KEY]))

    # create final content form
    meta_content = """

> [!TIP]
""" + "\n".join("> " + line for line in lines)
    return {OUTPUT_META_KEY: meta_content}


# helpers  #####################################################################

LLM2DISPLAY_NAME = {
    "rapid": "⚡Rapid",
    "chat": "💬Chat",
    "think": "🤔Think",
    "think-think": "🧠Think Think",
}


USAGE_TIME_KEY = "time_to_generate"


def _llm2display_name(llm):
    if llm in LLM2DISPLAY_NAME:
        return LLM2DISPLAY_NAME[llm]
    else:
        return llm  # fall back
