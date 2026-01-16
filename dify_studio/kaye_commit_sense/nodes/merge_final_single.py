# TODO


def main(
    filenames_list: list[str], per_file_extracts: list[dict]
):  # pylint: disable=missing-function-docstring
    filename = filenames_list[0]

    file_extract = per_file_extracts[0]

    symbol = file_extract["symbol"]
    summary = file_extract["summary"]

    opt = """{}

[{}]{}""".format(summary, symbol, filename)

    return {"result": opt}
