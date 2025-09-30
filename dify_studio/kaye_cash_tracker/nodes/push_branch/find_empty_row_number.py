def main(current_sheet: list[dict]):
    result = len(current_sheet[0]["valueRanges"][0]["values"]) + 1
    return {"result": result}
