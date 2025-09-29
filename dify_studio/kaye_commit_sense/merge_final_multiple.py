def main(primary: str, per_files: list[dict]):

    # create line per file
    lines = []
    for file in per_files:
        symbol = file["symbol"]
        file_name = file["file_name"]
        summary = file["summary"]
        line = "[{}]{}: {}".format(symbol, file_name, summary)
        lines.append(line)

    lines_text = "\n".join(lines)

    # combines
    opt = """{}

{}""".format(primary, lines_text)

    return {"result": opt}