# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_RESULT_KEY = "result"


# Entry Point  #################################################################
def main(
    allows_md: bool, filenames_list: list[str], per_file_extracts: list[dict]
):
    """
    merge to produce final output,
    when only single file is involved


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
    filename = filenames_list[0]
    file_extract = per_file_extracts[0]
    symbol = file_extract["symbol"]

    filename_line = ("{}`{}`" if allows_md else "{}[{}]").format(
        symbol, filename
    )

    summary = file_extract["summary"]

    opt = """{}

{}""".format(summary, filename_line)

    return {OUTPUT_RESULT_KEY: opt}
