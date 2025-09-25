def main(symbol: dict, file_name: dict, summary: dict):
    output = "[{}]{}:{}".format(symbol, file_name, summary)
    return {"result": output}
