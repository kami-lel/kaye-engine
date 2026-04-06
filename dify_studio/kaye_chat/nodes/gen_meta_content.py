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
        lines.append("Sensed:\t" + _generate_usage_line(sense_usage))

    # task parameters  ---------------------------------------------------------
    lines.append("Role:\t{}".format(current_role))
    lines.append("Difficulty:\t{}".format(current_difficulty))

    if current_role == "coder":
        lines.append("PLs:\t{}".format(current_pls))

    # task ---------------------------------------------------------------------
    lines.append("Task:")

    # FIXME task LLMs make difference
    # lines.append("LLM(s):\t{}".format(",".join(current_llms)))
    # lines.append("Task Usage(s):")
    # for usage in task_usages:
    #     lines.extend(_generate_usage_line(usage))

    # final content form  ------------------------------------------------------

    # create final content form
    meta_content = """

> [!TIP]
""" + "\n".join("> " + line for line in lines)
    return {OUTPUT_META_KEY: meta_content}
