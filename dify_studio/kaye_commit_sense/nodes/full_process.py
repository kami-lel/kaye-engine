import re

DIFF_GIT = "diff --git"
REGEX_PATTERN = r".+\/(.+)"


def main(input: str):
    filenames_list = []
    per_file_list = []

    for segment in input.split(DIFF_GIT)[1:]:
        filename = re.match(REGEX_PATTERN, segment).group(1)
        filenames_list.append(filename)

        per_line = DIFF_GIT + segment
        per_file_list.append(per_line)

    is_single_file = len(filenames_list) == 1

    return {
        "filenames_list": filenames_list,
        "per_file_list": per_file_list,
        "is_single_file": is_single_file,
    }
