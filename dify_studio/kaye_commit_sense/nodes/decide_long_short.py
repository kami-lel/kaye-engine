def main(
    item: str,
    long_short_threshold: float,
    per_file_change_long: str,
    per_file_change_short: str,
):
    newline_cnt = item.count("\n")
    is_long = newline_cnt > long_short_threshold

    return {
        "result": per_file_change_long if is_long else per_file_change_short
    }
