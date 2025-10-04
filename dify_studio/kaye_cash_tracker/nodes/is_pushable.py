OUTPUT_KEY = "is_pushable"


def main(input: str, push_trigger: str, transactions_array: dict):

    if push_trigger not in input:
        return {OUTPUT_KEY: False}

    rows = transactions_array.get("rows", [])
    for row in rows:
        for cell in row:
            if str(cell) == "???":  # match exact triple question marks
                return {OUTPUT_KEY: False}
    return {OUTPUT_KEY: True}  # return dict with success code
