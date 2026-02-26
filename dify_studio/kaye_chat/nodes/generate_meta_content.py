# pylint: disable=missing-module-docstring
# HACK deprecation


# output keys  #################################################################
OUTPUT_META_KEY = "meta_content"


# constants  ###################################################################
USAGE_TIME_KEY = "time_to_generate"


# Entry Point  #################################################################
def main(
    show_meta_content,
    pre_sense_usage,
):
    if not show_meta_content:
        return {OUTPUT_META_KEY: ""}  # skip

    lines = []
    # TODO write meta content generation

    # TODO in meta, use emoji for LLM

    # meta content form  -------------------------------------------------------
    meta_content = """

> [!TIP]
""" + "\n".join("> " + line for line in lines)

    return {OUTPUT_META_KEY: meta_content}
