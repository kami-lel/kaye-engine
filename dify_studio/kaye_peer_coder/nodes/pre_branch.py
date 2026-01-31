"""
- decide which branch/LLM to use depending on difficulty

- produce supplementary historical user/bot messages for this round
  (exclude this round's user message)

- produce prefix meta content


:param difficulty:
:type difficulty: int
:param difficulty_thresholds:
:type difficulty_thresholds: list[float]
:param languages:
:type languages: str
:param show_prefix_meta_content:
:type show_prefix_meta_content: bool
:return: {
        "llm": 0~2, which LLM to be used
        "supplement_user_messages": additional historical user messages
                that this model is unaware of
        "supplement_bot_messages": v.s.
        "prefix_meta_content": prefix meta content, may be empty
        "last_memory": updated last_memory
        }
:rtype: dict{
        "llm": int,
        "supplement_user_messages": str,
        "supplement_bot_messages": str,
        "prefix_meta_content": str,
        "last_memory": list[str]
        }
"""

# TODO update docstring

# output keys  #################################################################
OUTPUT_LLM_KEY = "llm"
OUTPUT_PREFIX_KEY = "prefix_meta_content"


# constants  ###################################################################
LLM_COUNT = 3  # number of LLMs
MESSAGE_SPLIT = "\n\n\n"


# Entry Point  #################################################################


def main(
    difficulty: int,
    difficulty_thresholds: list[float],
    languages: str,
    show_prefix_meta_content: bool,
    difficulty_override: float,
):  # pylint: disable=missing-function-docstring
    # decide branch  -----------------------------------------------------------
    if difficulty < difficulty_thresholds[0]:
        llm = 0
    elif difficulty < difficulty_thresholds[1]:
        llm = 1
    else:
        llm = 2

    # get prefix meta content  -------------------------------------------------
    prefix_content = ""
    if show_prefix_meta_content:
        prefix_content = """> [!TIP]
> difficulty_override: {} (usage: {})
> difficulty: {}
> languages: {}
> LLM: {}

""".format(
            difficulty_override,
            (0 <= difficulty_override <= 1),
            difficulty,
            languages,
            llm,
        )

    return {
        OUTPUT_LLM_KEY: llm,
        OUTPUT_PREFIX_KEY: prefix_content,
    }
