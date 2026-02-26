# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_META_KEY = "meta_content"


# Entry Point  #################################################################
def main(
    show_meta_content,
    role: str,
    llm_override: str,
    llm_sensed: dict,
    difficulty_override: float,
    difficulty_sensed: dict,
    sense_usage: dict,
    task_usage: dict,
):
    # TODO write meta content gen
    # TODO in meta, use emoji for LLM
    meta_content = ""
    return {OUTPUT_META_KEY: meta_content}


#     if show_prefix_meta_content:
#         content = """> [!TIP]
# > LLM: {}

# """.format(selection)

#     meta_content = """

# > [!TIP]
# """ + "\n".join("> " + line for line in lines)
