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

    safe_title = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", title)

    folder_name = "[{year}]{title}".format(year=year, title=safe_title)
    resource_name = "{" + folder_name + "}" + ",".join(tags)

    # create response  ---------------------------------------------------------
    if title == safe_title:
        title_part = "Title:\n```\n{}\n```\n".format(title)
    else:
        title_part = (
            "Title:\n```\n{}\n```\nTitle (Safe):\n```\n{}\n```\n".format(
                title, safe_title
            )
        )

    response = title_part + """
Folder Name:

```
{}
```

Resource Name:

```
{}
```
""".format(folder_name, resource_name)

    return {OUTPUT_RESPONSE_KEY: response}
