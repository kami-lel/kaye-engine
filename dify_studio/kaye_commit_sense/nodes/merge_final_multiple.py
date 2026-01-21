"""
merge to produce final output,
when multiple files are involved


:param allows_md: whether utilize md format in final result
:type allows_md: bool
:param primary_message:
:type primary_message: str
:param filenames_list:
:type filenames_list: list[str]
:param per_file_extracts:
:type per_file_extracts: list[dict]
:return: {"result": merged output}
:rtype: dict{"result": str}
"""

# config  ######################################################################
OUTPUT_RESULT_KEY = "result"


# Entry Point  #################################################################
def main(
    allows_md: bool,
    primary_message: str,
    filenames_list: list[str],
    per_file_extracts: list[dict],
):  # pylint: disable=missing-function-docstring
    line_pattern = "{}`{}` {}" if allows_md else "{}[{}] {}"

    # create line per file
    lines = []
    for filename, file_extract in zip(filenames_list, per_file_extracts):
        symbol = file_extract["symbol"]
        summary = file_extract["summary"]
        line = line_pattern.format(symbol, filename, summary)
        lines.append(line)

    # combines
    opt = """{}

{}""".format(primary_message, "\n".join(lines))

    return {OUTPUT_RESULT_KEY: opt}
