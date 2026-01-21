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

# output keys  #################################################################
OUTPUT_TRANSACTIONS_KEY = "transactions"
OUTPUT_TABLE_KEY = "transactions_table"

# constants  ###################################################################
TRANSACTIONS_KEY = "transactions"


def main(
    current_transactions: dict,
    extract_obj: dict,
):  # pylint: disable=missing-function-docstring

    # merge 2 transactions  ====================================================
    transactions_dict = {}  # dict with id -> entry
    # fill transactions_dict w/ current transactions

    for transaction in (
        current_transactions[TRANSACTIONS_KEY]  # add existing transactions
        + extract_obj[TRANSACTIONS_KEY]  # update/add new transactions
    ):
        tid = transaction[0]
        transactions_dict[tid] = transaction

    # convert dict to list
    transactions = sorted(
        transactions_dict.values(),
        key=lambda transaction: transaction[1],  # sort by date
        reverse=True,  # newest at top
    )

    # wrap in dict for correct returned type
    transactions_obj = {TRANSACTIONS_KEY: transactions}

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
        # make sure None -> '', and don't skip id field
        entries = [entry if entry is not None else "" for entry in row[1:]]
        line = "| " + " | ".join(entries) + " |"
        md_lines.append(line)

    transactions_table = "\n".join(md_lines)

    # returns ==================================================================
    return {
        OUTPUT_TRANSACTIONS_KEY: transactions_obj,
        OUTPUT_TABLE_KEY: transactions_table,
    }
