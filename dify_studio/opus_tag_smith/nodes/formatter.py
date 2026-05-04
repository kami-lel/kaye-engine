# pylint: disable=missing-module-docstring


import re

# constants  ###################################################################


EXTRACT_TITLE_KEY = "title"
EXTRACT_YEAR_KEY = "release_year"
EXTRACT_TAGS_KEY = "tags"


# Output Keys  #################################################################
OUTPUT_RESPONSE_KEY = "response"


# Entry Point  #################################################################
def main(extract: dict, target: str):
    """
    :param extract:
    :type extract: dict
    :param target: target/mode of operation, "Opus" or "Athenaeum"
    :type target: str
    :return: {
        "response": response formatted in md
    }
    :rtype: dict{"response": str}
    """

    title = extract[EXTRACT_TITLE_KEY]
    year = extract[EXTRACT_YEAR_KEY]
    tags = extract[EXTRACT_TAGS_KEY]

    filename = "[{year}]{title}{{{tags}}}".format(
        year=year, title=title, tags=",".join(tags)
    )
    safe_filename = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", filename)

    response = """```
{}
```
""".format(safe_filename)

    return {OUTPUT_RESPONSE_KEY: response}
