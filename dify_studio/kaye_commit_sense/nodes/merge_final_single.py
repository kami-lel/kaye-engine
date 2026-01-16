"""
merge to produce final output,
when only single file is involved


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
    filenames_list: list[str], per_file_extracts: list[dict]
):  # pylint: disable=missing-function-docstring
    filename = filenames_list[0]

    file_extract = per_file_extracts[0]

    symbol = file_extract["symbol"]
    summary = file_extract["summary"]

    opt = """{}

[{}]{}""".format(summary, symbol, filename)

    return {OUTPUT_RESULT_KEY: opt}
