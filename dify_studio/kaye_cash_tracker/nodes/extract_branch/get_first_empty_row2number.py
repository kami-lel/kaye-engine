# Todo module docstring


def main(current_sheet):  # pylint: disable=missing-function-docstring
    result = len(current_sheet[0]["valueRanges"][0]["values"]) + 1
    return {"result": result}
