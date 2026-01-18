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
:param dialogue_count:
:type dialogue_count: int
:param dialogue_count:
:type last_memory: list[int]
:param historical_user_messages:
:type historical_user_messages: list[str]
:param historical_bot_messages:
:type historical_bot_messages: list[str]
:param show_prefix_meta_content:
:type show_prefix_meta_content: bool
:return: {
        "branch": 0~2, which LLM to be used
        "supplement_user_messages": additional historical user messages
                that this model is unaware of
        "supplement_bot_messages": v.s.
        "prefix_meta_content": prefix meta content, may be empty
        }
:rtype: dict{
        "branch": int,
        "supplement_user_messages": str,
        "supplement_bot_messages": str,
        "prefix_meta_content": str,
        }
"""

# constants  ###################################################################
OUTPUT_BRANCH_KEY = "branch"
OUTPUT_USER_KEY = "supplement_user_messages"
OUTPUT_BOT_KEY = "supplement_bot_messages"
OUTPUT_PREFIX_KEY = "prefix_meta_content"
OUTPUT_MEMORY_KEY = "last_memory"


# Entry Point  #################################################################


def main(
    difficulty: int,
    difficulty_thresholds: list[float],
    languages: str,
    dialogue_count: int,
    last_memory: list[int],
    historical_user_messages: list[str],
    historical_bot_messages: list[str],
    show_prefix_meta_content: bool,
):  # pylint: disable=missing-function-docstring
    # decide branch  -----------------------------------------------------------
    if difficulty < difficulty_thresholds[0]:
        branch = 0
    elif difficulty < difficulty_thresholds[1]:
        branch = 1
    else:
        branch = 2

    # generate historical messages  --------------------------------------------

    # TODO
    historical_user_message = ""
    historical_bot_message = ""
    # TODO update last_memory

    # decide prefix  -----------------------------------------------------------
    prefix_content = ""
    if show_prefix_meta_content:
        prefix_content = """> difficulty: {}
> languages: {}
> LLM used: {}


""".format(difficulty, languages, branch)

    return {
        OUTPUT_BRANCH_KEY: branch,
        OUTPUT_USER_KEY: historical_user_message,
        OUTPUT_BOT_KEY: historical_bot_message,
        OUTPUT_MEMORY_KEY: last_memory,
        OUTPUT_PREFIX_KEY: prefix_content,
    }
