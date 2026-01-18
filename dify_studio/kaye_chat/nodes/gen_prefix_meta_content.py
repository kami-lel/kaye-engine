"""
create prefix meta content


:param selection:
:type selection: str
:param show_prefix_meta_content:
:type show_prefix_meta_content: bool
:return: {
        "prefix_meta_content": may be empty
        }
:rtype: dict{
        "prefix_meta_content": str
        }
"""

# constants  ###################################################################
OUTPUT_PREFIX_KEY = "prefix_meta_content"


# Entry Point  #################################################################


def main(
    selection: dict, show_prefix_meta_content: bool
):  # pylint: disable=missing-function-docstring
    content = ""

    if show_prefix_meta_content:
        content = """[!TIP]
> LLM: {}

""".format(selection)

    return {OUTPUT_PREFIX_KEY: content}
