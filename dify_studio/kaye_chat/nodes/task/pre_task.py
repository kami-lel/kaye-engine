# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments


import json

# Output Key ###################################################################
OUTPUT_BODY_KEY = "task_prompt_getter_body"
OUTPUT_LLMS_KEY = "llms"
OUTPUT_MEMORY_KEY = "difficulties_memory"
OUTPUT_DECAYED_KEY = "decayed_difficulty"
OUTPUT_USED_KEY = "used_difficulty"
OUTPUT_DIRECT_KEY = "is_direct_response"


# constants  ###################################################################
THRESHOLDS = [
    (0, ["gpt-4-nano"]),
    (10, ["gpt-5-nano"]),
    (30, ["claude-sonnet-4"]),
    (60, ["claude-sonnet-4", "gpt-5-mini"]),
    (80, ["claude-opus-4", "gpt-5"]),
    (90, ["claude-opus-4", "gpt-5", "gemini-3-pro"]),
]
# (lower bounds, LLMs to use)


# number of rounds to remember difficulties
DIFFICULTY_MEMORY_CNT = 8

# Exponential Moving Average: Alpha, smoothing factor
EMA_ALPHA = 0.6


# Entry Point  #################################################################
def main(
    query: str,
    current_role: str,
    current_pls: str,
    difficulties_memory: list[int],
    current_difficulty: int,
):
    """
    :param query:
    :type query: str
    :param current_role:
    :type current_role: str
    :param current_pls:
    :type current_pls: str
    :param difficulty:
    :type difficulty: int
    :return: {
        "task_prompt_getter_body":  body sent to /task
        "llms":                     LLMs to use during tasks
        "difficulties_memory"
        "is_direct_response":       whether use direct response mode during task
    }

    :rtype: dict{
        "task_prompt_getter_body":  str,
        "llms":                     list[str],
        "difficulties_memory":      list[int],
        "is_direct_response":       bool,
    }
    """

    # gen body  ----------------------------------------------------------------
    # used for Task Prompt Getter node

    body = {
        "query": query,
        "role": current_role,
        "programming_languages": current_pls,
    }
    body_json_dumps = json.dumps(body)

    # decaying difficulty  -----------------------------------------------------
    difficulties_memory.append(int(current_difficulty))
    # keep only recent (last) rounds
    difficulties_memory = difficulties_memory[-DIFFICULTY_MEMORY_CNT:]

    # calc decaying difficulty
    ema = float(difficulties_memory[0]) if difficulties_memory else 0.0
    for d in difficulties_memory[1:]:
        ema = EMA_ALPHA * d + (1.0 - EMA_ALPHA) * ema
    decayed_difficulty = max(1, min(100, round(ema)))

    # always use higher value of two
    used_difficulty = max(current_difficulty, decayed_difficulty)

    # decide LLMs to use  ------------------------------------------------------
    llms = THRESHOLDS[0][1]
    for threshold, value in THRESHOLDS:
        if used_difficulty >= threshold:
            llms = value

    # is direct  ---------------------------------------------------------------
    is_direct_response = len(llms) == 1

    # Output Variables  --------------------------------------------------------
    return {
        OUTPUT_BODY_KEY: str(body_json_dumps),
        OUTPUT_LLMS_KEY: llms,
        OUTPUT_MEMORY_KEY: difficulties_memory,
        OUTPUT_DIRECT_KEY: bool(is_direct_response),
        OUTPUT_DECAYED_KEY: decayed_difficulty,
        OUTPUT_USED_KEY: used_difficulty,
    }
