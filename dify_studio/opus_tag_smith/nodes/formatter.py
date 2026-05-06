# pylint: disable=missing-module-docstring


import re

# constants  ###################################################################


EXTRACT_TITLE_KEY = "title"
EXTRACT_YEAR_KEY = "release_year"
EXTRACT_TAGS_KEY = "tags"
EXTRACT_SEASON_KEY = "season_number"
EXTRACT_EPISODE_KEY = "episode_number"
EXTRACT_EPISODE_NAME_KEY = "episode_name"


# Output Keys  #################################################################
OUTPUT_RESPONSE_KEY = "response"


# helpers  #####################################################################


def _format_opus(extract):  # ==================================================
    title = extract[EXTRACT_TITLE_KEY]
    year = extract[EXTRACT_YEAR_KEY]
    tags = extract[EXTRACT_TAGS_KEY]

    # season & episode  --------------------------------------------------------
    season_and_episode = []
    season_number = extract.get(EXTRACT_SEASON_KEY)
    if season_number:
        season_and_episode.append("S{}".format(season_number))

    episode_number = extract.get(EXTRACT_EPISODE_KEY)
    if episode_number:
        if season_number:
            season_and_episode.append(".")

        season_and_episode.append("E{}".format(episode_number))

        episode_name = extract.get(EXTRACT_EPISODE_NAME_KEY)
        if episode_name:
            season_and_episode.append("-")
            season_and_episode.append(episode_name)

    season_and_episode_content = ""
    if len(season_and_episode) > 0:
        season_and_episode_content = "".join(season_and_episode)
        title = title + "." + season_and_episode_content

    # title names  -------------------------------------------------------------
    safe_title = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", title)
    folder_name = "[{year}]{title}".format(year=year, title=safe_title)
    resource_name = folder_name + "{" + ",".join(tags) + "}"

    # create response  ---------------------------------------------------------
    if title == safe_title:
        title_part = "Title:\n```\n{}\n```\n".format(title)
    else:
        title_part = (
            "Title:\n```\n{}\n```\nTitle (Safe):\n```\n{}\n```\n".format(
                title, safe_title
            )
        )

    sne_part = ""
    if season_and_episode_content:
        sne_part = """Episode Name:

```
{}
```
""".format(season_and_episode_content)

    response = title_part + sne_part + """
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


def _format_athe(extract):  # ==================================================
    pass


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
