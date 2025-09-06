def main(transactions):
    for item in transactions:
        row = item.get("row", [])  # get row list or empty list
        for cell in row:
            if str(cell) == "???":  # match exact triple question marks
                return {"result": 0}  # return dict with failure code
    return {"result": 1}  # return dict with success code
