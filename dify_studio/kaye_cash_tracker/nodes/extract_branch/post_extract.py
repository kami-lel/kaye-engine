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
    "transactions": merged
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
    for transaction in current_transactions[TRANSACTIONS_KEY]:
        tid = transaction[0]  # get id as 1st entry of list
        transactions_dict[tid] = transaction

    # update transactions_dict with newly extracted entries
    for transaction in extract_obj[TRANSACTIONS_KEY]:
        tid = transaction[0]
        transactions_dict[tid] = transaction

    # convert dict to list, sorted by date
    # TODO
    transactions = []

    # wrap in dict for correct returned type
    transactions_obj = {TRANSACTIONS_KEY: transactions}

    # create MD table  =========================================================
    # BUG
    # Generate header row with updated headers
    header = ["", "¤", "Out", "In", "From", "To", "", "Remarks"]
    # Separator line for markdown table formatting
    separator = ["---"] * 8
    # Initialize list for markdown lines including header
    md_lines = []
    md_lines.append("| " + " | ".join(header) + " |")
    md_lines.append("| " + " | ".join(separator) + " |")

    # Fill in data rows from spreadsheet
    for row in transactions_obj.get("rows", []):
        # Replace None entries with empty string
        row_processed = [entry if entry is not None else "" for entry in row]
        md_lines.append("| " + " | ".join(row_processed) + " |")
    transactions_table = "\n".join(md_lines)

    return {
        OUTPUT_TRANSACTIONS_KEY: transactions_obj,
        OUTPUT_TABLE_KEY: transactions_table,
    }
