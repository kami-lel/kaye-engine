def main(
    item: str,
    long_short_threshold: float,
    prompt_per_file_extract_long: str,
    prompt_per_file_extract_short: str,
):
    newline_cnt = item.count("\n")
    is_long = newline_cnt > long_short_threshold

    return {
        "extract_prompt": (
            prompt_per_file_extract_long
            if is_long
            else prompt_per_file_extract_short
        )
    }
