# pylint: disable=missing-module-docstring


import re

# output keys  #################################################################
OUTPUT_FILENAME_LIST_KEY = "filenames_list"
OUTPUT_PER_FILE_LIST_KEY = "per_file_list"
OUTPUT_IS_SINGLE_FILE_KEY = "is_single_file"
OUTPUT_ALLOWS_MD_KEY = "allows_md"
OUTPUT_ALLOWS_MD_NUMBER_KEY = "allows_md_number"

# constants  ###################################################################
DIFF_GIT = "diff --git"
REGEX_PATTERN = r".+\/(.+)"


# Entry Point  #################################################################
def main(content: str, allows_md: bool):
    """
    perform pre-process directly on inputs:

    - split the full diff content per file
    - decide if there is only one file change
    - pass through ``allows_md`` as both Boolean and number


    :param content:
    :type content: str
    :param allows_md:
    :type allows_md: bool
    :return: {
        "filename_list": a list of all files' name
        "per_file_list": a list of all files' diff content
        "is_single_file": if the given content contains only single file
    }
    :rtype: dict{
        "filename_list": list[str]
        "per_file_list": list[str]
        "is_single_file": bool
    }
    """
    filenames_list = []
    per_file_list = []

    for segment in content.split(DIFF_GIT)[1:]:
        filename = re.match(REGEX_PATTERN, segment).group(1)
        filenames_list.append(filename)

        per_line = DIFF_GIT + segment
        per_file_list.append(per_line)

    is_single_file = len(filenames_list) == 1

    return {
        OUTPUT_FILENAME_LIST_KEY: filenames_list,
        OUTPUT_PER_FILE_LIST_KEY: per_file_list,
        OUTPUT_IS_SINGLE_FILE_KEY: is_single_file,
        OUTPUT_ALLOWS_MD_KEY: allows_md,
        OUTPUT_ALLOWS_MD_NUMBER_KEY: 1 if allows_md else 0,
    }
