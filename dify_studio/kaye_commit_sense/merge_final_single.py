def main(per_files: list[dict]):
    file = per_files[0]  # only single file
    file_name = file['file_name']
    symbol = file['symbol']
    summary = file['summary']

    opt = """{}
    
[{}]{}""".format(summary, symbol, file_name)

    return {"result": opt}