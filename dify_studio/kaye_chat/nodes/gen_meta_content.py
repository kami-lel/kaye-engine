# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments


# output keys  #################################################################
OUTPUT_META_KEY = "meta_content"


# constants  ###################################################################
USAGE_TIME_KEY = "time_to_generate"
USAGE_TOKEN_KEY = "total_tokens"


# helpers  #####################################################################
def _generate_usage_lines(usage):
    return ["%%%"]  # TODO


# Entry Point  #################################################################


def main(
    show_meta_content,
    should_skip_sense,
    current_role: str,
    current_difficulty: float,
    current_llms: list[str],
    current_pls: str,
    sense_usage: dict,
    task_usages: list[dict],
):
    if not show_meta_content:
        return {OUTPUT_META_KEY: ""}

    lines = []

    # sense-related  -----------------------------------------------------------
    if should_skip_sense:
        lines.append("(Sense Skipped)")
    else:
        lines.append("Sensed")
        lines.extend(_generate_usage_lines(sense_usage))

    # task parameters  ---------------------------------------------------------
    lines.append("role:\t{}".format(current_role))
    lines.append("difficulty:\t{}".format(current_difficulty))
    lines.append("LLMs:\t{}".format(",".join(current_llms)))

    if current_role == "coder":
        lines.append("PLs:\t{}".format(current_pls))

    # task usages  -------------------------------------------------------------
    lines.append("Task Usage(s):")
    for usage in task_usages:
        lines.extend(_generate_usage_lines(usage))

    # final content form  ------------------------------------------------------

    # create final content form
    meta_content = """

> [!TIP]
""" + "\n".join("> " + line for line in lines)
    return {OUTPUT_META_KEY: meta_content}


# HACK rm

#     """
#     generate **meta content**, information for debugging and testing


#     :param show_meta_content: whether to show meta content,
#             set as User Input Field
#     :type show_meta_content: bool
#     :param role_override:
#     :type role_override: str
#     :param role:
#     :type role: str
#     :param llm_override:
#     :type llm_override: str
#     :param llm_used:
#     :type llm_used: str
#     :param difficulty_override:
#     :type difficulty_override: float
#     :param difficulty_sensed:
#     :type difficulty_sensed: float
#     :param skip_sense:
#     :type skip_sense: bool
#     :param programming_languages:
#     :type programming_languages: str
#     :param sense_usage: usage object for information of sense node
#     :type sense_usage: dict
#     :param task_usage: usage object for information of task node
#     :type task_usage: dict
#     """
#     if not show_meta_content:
#         return {OUTPUT_META_KEY: ""}

#     lines = []

#     # create role line
#     if role_override:
#         lines.append("Role (Override): {}".format(role_override))
#     else:
#         lines.append("Role: {}".format(role))

#     # create llm line
#     if llm_override:
#         lines.append(
#             "LLM (Override): {}".format(_llm2display_name(llm_override))
#         )
#     else:
#         lines.append("LLM: {}".format(_llm2display_name(llm_used)))

#     role_used = role_override or role
#     if role_used == "coder":
#         if difficulty_override == -1:
#             lines.append("Difficulty: {}".format(difficulty_sensed))
#         else:
#             lines.append(
#                 "Difficulty (Override): {}".format(difficulty_override)
#             )

#         lines.append("PLs: {}".format(programming_languages))

#     if not skip_sense:
#         lines.append("Sense: {}s".format(sense_usage[USAGE_TIME_KEY]))

#     lines.append("Task: {}s".format(task_usage[USAGE_TIME_KEY]))
