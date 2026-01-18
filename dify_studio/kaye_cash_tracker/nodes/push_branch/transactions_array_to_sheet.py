# todo docstring


def main(
    transactions_array: dict, google_sheet_name: str, empty_row_number: float
):  # pylint: disable=missing-function-docstring
    rows_from = transactions_array["rows"]

    end_range_row = empty_row_number + len(rows_from) - 1

    # generate range
    sheet_range = "{}!A{}:H{}".format(
        google_sheet_name, empty_row_number, end_range_row
    )

    # generate values
    rows_to = []
    for row in rows_from:
        current_row = []
        for i, col in enumerate(row):
            if i in (2, 3) and col:  # amount in/out
                # convert to number for amount in/out col, when not empty
                current_row.append(col)
            else:  # string entry
                current_row.append('"{}"'.format(col))

        row_content = ",".join(current_row)
        rows_to.append(row_content)

    values = "[{}]".format(",".join("[{}]".format(row) for row in rows_to))

    result = '[{{"range": "{}", "values": {}}}]'.format(sheet_range, values)

    return {"result": result}
