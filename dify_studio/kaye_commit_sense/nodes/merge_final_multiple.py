# todo module docstring


def main(
    primary_message: str,
    filenames_list: list[str],
    per_file_extracts: list[dict],
):  # pylint: disable=missing-function-docstring
    # create line per file
    lines = []
    for filename, file_extract in zip(filenames_list, per_file_extracts):
        symbol = file_extract["symbol"]
        summary = file_extract["summary"]
        line = "[{}]{}: {}".format(symbol, filename, summary)
        lines.append(line)

    # combines
    opt = """{}

{}""".format(primary_message, "\n".join(lines))

    return {"result": opt}
