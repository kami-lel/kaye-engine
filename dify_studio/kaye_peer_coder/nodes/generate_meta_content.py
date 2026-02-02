"""
generate the meta conten


:param show_meta_content:
:type show_meta_content: bool
:param difficulty_override:
:type difficulty_override: float
:param difficulty:
:type difficulty: float
:param languages:
:type languages: str
:param llm:
:type llm: str
:param pre_sense_usage:
:type pre_sense_usage: dict
:param llm_usage:
:type llm_usage: dict
"""

# output keys  #################################################################
OUTPUT_META_KEY = "meta_content"


# constants  ###################################################################
USAGE_TIME_KEY = "time_to_generate"


def main(
    show_meta_content: bool,
    difficulty_override: float,
    difficulty: float,
    languages: str,
    llm: str,
    pre_sense_usage: dict,
    llm_usage: dict,
):  # pylint: disable=missing-function-docstring,
    # pylint: disable=too-many-positional-arguments,too-many-arguments
    if not show_meta_content:
        return {OUTPUT_META_KEY: ""}  # skip

    lines = []

    # update formats to be printed
    use_difficulty_override = 0 <= difficulty_override <= 1

    if use_difficulty_override:
        lines.append("difficulty_override: {}".format(difficulty_override))
    else:
        # use pre-sense
        lines.append(
            "pre-sense [{}]s: difficulty: {}".format(
                pre_sense_usage[USAGE_TIME_KEY], difficulty
            )
        )
        if languages:
            lines.append("languages: {}".format(languages))

    # line re the LLM
    llm_time = llm_usage[USAGE_TIME_KEY]
    lines.append("{} [{}]s".format(llm, llm_time))

    # > difficulty_override: {} (usage: {})
    # > difficulty: {}
    # > languages: {}
    # > pre-sense time: {}
    # > task time: {}s

    # form final format  -------------------------------------------------------
    meta_content = """

> [!TIP]
""" + "\n".join("> " + line for line in lines)
    return {OUTPUT_META_KEY: meta_content}
