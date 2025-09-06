def main(spreadsheet):
    # Generate header row with updated headers
    header = ["", "¤", "Out", "In", "from", "To", "", "Remark"]
    # Separator line for markdown table formatting
    separator = ["---"] * 8
    # Initialize list for markdown lines including header
    md_lines = []
    md_lines.append("| " + " | ".join(header) + " |")
    md_lines.append("| " + " | ".join(separator) + " |")
    # Fill in data rows from spreadsheet
    for row in spreadsheet.get("rows", []):
        md_lines.append("| " + " | ".join(row) + " |")
    # Join all lines into a single markdown table string
    md_table = "\n".join(md_lines)
    return {"result": md_table}