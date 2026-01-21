"""
post extract node, perform:

- merge extracted transactions (``extract_obj``)
  with existing transactions (``current_transactions``)

- create a MD-formatted table


:param current_transactions:
:type current_transactions: dict
:param extract_obj:
:type extract_obj: dict
:return: {
    "transactions": merged transactions
    "transactions_table":
}
:rtype: dict{
    "transactions": dict
    "transactions_table": str
}
"""

import json

# output keys  #################################################################
OUTPUT_TRANSACTIONS_KEY = "transactions"
OUTPUT_TABLE_KEY = "transactions_table"

# constants  ###################################################################
ROWS_KEY = "rows"


def main(
    current_transactions: str,
    extracted_rows: list,
):  # pylint: disable=missing-function-docstring

    # merge 2 transactions  ====================================================
    # merge 2 transactions as a 2D array
    rows_array = []
    # add current transactions
    if current_transactions:
        rows_array.extend(json.loads(current_transactions))

    # add updated transactions
    rows_array.extend(extracted_rows)

    rows_dict = {}  # use dict to merge by id/keys
    for row in rows_array:
        tid = row[0]
        rows_dict[tid] = row

    # convert dict to list
    transactions = sorted(
        rows_dict.values(),
        key=lambda transaction: transaction[1],  # sort by date
        reverse=True,  # newest at top
    )

    # serialize as json string to store
    transactions_obj = json.dumps(transactions)

    # create MD table  =========================================================
    # generate header row with updated headers
    header = ["", "¤", "Out", "In", "From", "To", "", "Remarks"]
    # Separator line for markdown table formatting
    separator = ["---"] * 8
    # Initialize list for markdown lines including header
    md_lines = []
    md_lines.append("| " + " | ".join(header) + " |")
    md_lines.append("| " + " | ".join(separator) + " |")

    # Fill in data rows from spreadsheet
    for row in transactions:
        # make sure None -> '', and skip id field
        entries = [entry if entry is not None else "" for entry in row[1:]]
        line = "| " + " | ".join(entries) + " |"
        md_lines.append(line)

    transactions_table = "\n".join(md_lines)

    # returns ==================================================================
    return {
        OUTPUT_TRANSACTIONS_KEY: transactions_obj,
        OUTPUT_TABLE_KEY: transactions_table,
    }
