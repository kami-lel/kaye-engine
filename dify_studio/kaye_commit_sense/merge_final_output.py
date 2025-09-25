def main(primary: str, per_files: list[str]):

    lines = "\n".join(per_files)
    opt = """{}

{}""".format(primary, lines)

    return {"result": opt}
