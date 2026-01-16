# todo module docstring

OUTPUT_KEY = "is_push_legal"


def main(
    input: str, transactions_array: dict
):  # pylint: disable=missing-function-docstring
    """
    decide whetehr if making a push with current `transactions_array` is legal


    :param input:
    :type input: str
    :param transactions_array:
    :type transactions_array: dict
    :return: value of entry `is_push_legal` is a `bool`
    :rtype: dict
    """

    rows = transactions_array.get("rows", [])

    for row in rows:
        for cell in row:
            if str(cell) == "???":  # match exact triple question marks
                return {OUTPUT_KEY: False}

    return {OUTPUT_KEY: True}  # return dict with success code
