"""
decide which branch/LLM to use for branching, also generate prefix meta content


:param difficulty:
:type difficulty: float
:param difficulty_thresholds: a list of thresholds, exclude 0.0 & 1.0
:type difficulty_thresholds: list[float]
:param show_prefix_meta_content:
:type show_prefix_meta_content: bool
:param languages:
:type languages: str
:return: {
        "branch": 0~2, which LLM/branch should be used
        "prefix_meta_content": may be empty
        }
:rtype: dict{
        "branch": int
        "prefix_meta_content": str
        }
"""

# constants  ###################################################################
OUTPUT_BRANCH_KEY = "branch"
OUTPUT_PREFIX_KEY = "prefix_meta_content"


# Entry Point  #################################################################


def main(
    difficulty: float,
    difficulty_thresholds: list[float],
    show_prefix_meta_content,
    languages: str,
):  # pylint: disable=missing-function-docstring
    # decide branch  ------------------------------------------------------------
    if difficulty < difficulty_thresholds[0]:
        branch = 0
    elif difficulty < difficulty_thresholds[1]:
        branch = 1
    else:
        branch = 2

    # decide prefix    ---------------------------------------------------------
    prefix_content = ""
    if show_prefix_meta_content:
        prefix_content = """> difficulty = {}
> languages = {}
> LLM used = {}


""".format(difficulty, languages, branch)

    return {OUTPUT_BRANCH_KEY: branch, OUTPUT_PREFIX_KEY: prefix_content}
