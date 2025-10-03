def main(filenames_list: list[str], per_file_extracts: list[dict]):
    filename = filenames_list[0]

    file_extract = per_file_extracts[0]

    symbol = file_extract["symbol"]
    summary = file_extract["summary"]

    opt = """{}

[{}]{}""".format(summary, symbol, filename)

    return {"result": opt}
