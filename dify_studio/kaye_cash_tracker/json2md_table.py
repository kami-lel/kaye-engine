def main(transactions):
    # todo docstring
    # Generate header row with updated headers
    header = ["", "¤", "Out", "In", "From", "To", "", "Remarks"]
    # Separator line for markdown table formatting
    separator = ["---"] * 8
    # Initialize list for markdown lines including header
    md_lines = []
    md_lines.append("| " + " | ".join(header) + " |")
    md_lines.append("| " + " | ".join(separator) + " |")

    # Fill in data rows from spreadsheet
    for row in transactions.get("rows", []):
        # Replace None entries with empty string
        row_processed = [entry if entry is not None else "" for entry in row]
        md_lines.append("| " + " | ".join(row_processed) + " |")
    md_table = "\n".join(md_lines)
    return {"result": md_table}
