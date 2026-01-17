# constants  ###################################################################
OUTPUT_BRANCH_KEY = "branch"
OUTPUT_PREFIX_KEY = "prefix_meta_content"


# Entry Point  #################################################################


def main(
    difficulty: float,
    difficulty_thresholds: list[float],
    show_prefix_meta_content,
    languages: str,
):
    # TODO docstring
    # BUG need test functionality
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
> branch = {}
""".format(difficulty, languages, branch)

    return {OUTPUT_BRANCH_KEY: branch, OUTPUT_PREFIX_KEY: prefix_content}
