# pylint: disable=missing-module-docstring


# output keys  #################################################################

OUTPUT_SKIP_PRIMARY = "skip_primary_message"
OUTPUT_ALLOWS_MD_API = "allows_md_query_value"
OUTPUT_PER_FILE_DIFF = "per_file_diff"


# constants  ###################################################################
DIFF_GIT = "diff --git"


# Entry Point  #################################################################
def main(content: str, allows_md: bool):
    """
    perform pre-process directly on inputs:

    - split the full diff content per file
    - decide if there is only one file change, to skip the primary message
    - pass through ``allows_md`` as ``1/2`` as URL query parameter value


    :param content:
    :type content: str
    :param allows_md:
    :type allows_md: bool
    :return: {
        "skip_primary_message": if the given content contains only single file
        "allows_md_query_value": old query value of ``allows_md_number``
        "per_file_diff": a list of all files' diff content
    }
    :rtype: dict{
        "skip_primary_message": bool
        "allows_md_query_value": int
        "per_file_diff": list[str]
    }
    """
    per_file_diff = []

    for segment in content.split(DIFF_GIT)[1:]:
        per_file_diff.append(DIFF_GIT + segment)

    skip_primary_message = len(per_file_diff) == 1

    return {
        OUTPUT_SKIP_PRIMARY: skip_primary_message,
        OUTPUT_ALLOWS_MD_API: 1 if allows_md else 0,
        OUTPUT_PER_FILE_DIFF: per_file_diff,
    }
