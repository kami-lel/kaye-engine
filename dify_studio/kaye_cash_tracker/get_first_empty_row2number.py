def main(current_sheet):
    # todo docstring
    result = int(current_sheet[0]["valueRanges"][0]["values"][0][0])
    return {"result": result}
