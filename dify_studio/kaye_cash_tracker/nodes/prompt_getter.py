"""
generate prompt via Kaye flask API, then caches it locally
"""

OUTPUT_PROMPT_KEY = "extract_info_prompt"


def main(extract_info_prompt_cache: str):
    if extract_info_prompt_cache:
        # prompt already in cache, use it
        return {OUTPUT_PROMPT_KEY: extract_info_prompt_cache}

    prompt = ""  # TODO
    return {OUTPUT_PROMPT_KEY: prompt}
