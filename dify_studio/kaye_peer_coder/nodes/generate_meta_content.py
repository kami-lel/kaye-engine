"""
TODO


:param show_meta_content:
:type show_meta_content: bool
:param difficulty_override:
:type difficulty_override: float
:param difficulty:
:type difficulty: float
:param languages:
:type languages: str
:param llm:
:type llm: float
:param pre_sense_usage:
:type pre_sense_usage: dict
:param llm_usage:
:type llm_usage: dict
"""

# output keys  #################################################################
OUTPUT_META_KEY = "meta_content"


# constants  ###################################################################
LLM_INDEX2NAME = {0: "LLM I", 1: "LLM II", 2: "LLM III"}
USAGE_TIME_KEY = "time_to_generate"


def main(
    show_meta_content: bool,
    difficulty_override: float,
    difficulty: float,
    languages: float,
    llm: float,
    pre_sense_usage: dict,
    llm_usage: dict,
):  # pylint: disable=missing-function-docstring
    if not show_meta_content:
        return {OUTPUT_META_KEY: ""}  # skip

    # update formats to be printed
    use_difficulty_override = 0 <= difficulty_override <= 1
    llm_name = LLM_INDEX2NAME[int(llm)]
    pre_sense_time = (
        "n/a" if use_difficulty_override else pre_sense_usage[USAGE_TIME_KEY]
    )
    llm_time = llm_usage[USAGE_TIME_KEY]

    # form final format  -------------------------------------------------------
    meta_content = """

> [!TIP]
> difficulty_override: {} (usage: {})
> difficulty: {}
> languages: {}
> branch: {}
> pre-sense time: {}s
> LLM time: {}s""".format(
        difficulty_override,
        use_difficulty_override,
        difficulty,
        languages,
        llm_name,
        pre_sense_time,
        llm_time,
    )

    return {OUTPUT_META_KEY: meta_content}


# BUG on 2nd round issue?
