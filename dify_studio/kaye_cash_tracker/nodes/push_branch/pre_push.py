"""
create ``data`` for push node


:param transactions:
:type transactions: str
:param column_a:
:type column_a: list[dict]
:param google_sheet_name:
:type google_sheet_name: str
:return: first empty row (first available row) in current sheet
:rtype: int
"""

import json

OUTPUT_DATA_KEY = "data"


def main(
    transactions: str,
    column_a: list[dict],
    google_sheet_name: str,
):  # pylint: disable=missing-function-docstring
    transactions_array = json.loads(transactions)
    # create ranges  ===========================================================
    # find range's row start, i.e. first empty row
    range_row_start = len(column_a[0]["valueRanges"][0]["values"]) + 1
    range_row_end = range_row_start + len(transactions_array) - 1
    ranges = "{}!A{}:H{}".format(
        google_sheet_name, range_row_start, range_row_end
    )

    # create values  ===========================================================
    rows = []
    for row in transactions_array:
        current_row = []
        for i, v in enumerate(row):
            if i == 0:
                continue  # skip id
            elif i in (3, 4):  # amount in/out
                # enter as number
                current_row.append(float(v))
            else:
                # enter as str
                current_row.append(v)

        rows.append(current_row)

    # create data  =============================================================
    data = [{"range": ranges, "values": rows}]
    data_json = json.dumps(data)
    return {OUTPUT_DATA_KEY: data_json}
