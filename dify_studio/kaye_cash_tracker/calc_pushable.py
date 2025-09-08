def main(transactions):
    # todo docstring
    rows = transactions.get("rows", [])
    for row in rows:
        for cell in row:
            if str(cell) == "???":  # match exact triple question marks
                return {"result": 0}  # return dict with failure code
    return {"result": 1}  # return dict with success code
