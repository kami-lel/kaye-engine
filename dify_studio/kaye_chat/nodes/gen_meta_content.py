# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_META_KEY = "meta_content"


# Entry Point  #################################################################
def main(
    show_meta_content,
    role_override,
    role,
    llm_override,
    llm_sensed,
    difficulty_override,
    difficulty_sensed,
    skip_sense,
    sense_usage,
    task_usage,
):
    if not show_meta_content:
        return {OUTPUT_META_KEY: ""}

    lines = []

    # create role line
    if role_override:
        lines.append("Role Override: {}".format(role_override))
    else:
        lines.append("Role: {}".format(role))

    # create llm line
    if llm_override:
        lines.append("LLM Override: {}".format(_llm2display_name(llm_override)))
    else:
        lines.append("LLM: {}".format(_llm2display_name(llm_sensed)))

    role_used = role_override or role
    if role_used == "peer_coder":
        if difficulty_override:
            lines.append("Difficulty Override: {}".format(difficulty_override))
        else:
            lines.append("Difficulty: {}".format(difficulty_sensed))

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
