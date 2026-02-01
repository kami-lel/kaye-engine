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


def main(
    show_meta_content: bool,
    difficulty_override: float,
    difficulty: float,
    languages: float,
    llm: float,
    pre_sense_usage: dict,
    llm_usage: dict,
):
    if not show_meta_content:
        return {OUTPUT_META_KEY: ""}

    # get prefix meta content  -------------------------------------------------
    use_difficulty_override = 0 <= difficulty_override <= 1

    prefix_content = ""
    if show_meta_content:
        prefix_content = """

> [!TIP]
> difficulty_override: {} (usage: {})
> difficulty: {}
> languages: {}
> pre-sense time: {}
> LLM: {}
> LLM time: {}

"""

    # form final format  -------------------------------------------------------

    meta_content = ""  # TODO

    return {OUTPUT_META_KEY: meta_content}
