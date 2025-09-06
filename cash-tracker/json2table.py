def main(transactions):
    header = [
        "",
        "¤",
        "Out",
        "In",
        "from",
        "To",
        "",
        "Remark",
    ]  # header init with Updated Headers
    separator = ["---"] * 8  # separator set for Markdown Table
    md_lines = []  # init markdown lines with Header
    md_lines.append("| " + " | ".join(header) + " |")  # append header line
    md_lines.append(
        "| " + " | ".join(separator) + " |"
    )  # append separator line
    for item in transactions:  # iterate Transactions list
        row = item.get("row", [])  # get row list or empty list
        str_cells = [str(cell) for cell in row]
        md_lines.append("| " + " | ".join(str_cells) + " |")  # append data row
    md_table = "\n".join(md_lines)  # join lines into single Markdown string
    return {"result": md_table}
