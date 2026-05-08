# pylint: disable=missing-module-docstring


import re

# constants  ###################################################################

SEP = ","


# extract keys  ################################################################


EXTRACT_TITLE_KEY = "title"
EXTRACT_YEAR_KEY = "release_year"
EXTRACT_TAGS_KEY = "tags"

# opus extract
EXTRACT_SEASON_KEY = "season_number"
EXTRACT_EPISODE_KEY = "episode_number"
EXTRACT_EPISODE_NAME_KEY = "episode_name"

# shelver extract
EXTRACT_AUTHOR_KEY = "authors"
EXTRACT_EDITOR_KEY = "editors"
EXTRACT_TRANSLATOR_KEY = "translators"
EXTRACT_PUBLISHER_KEY = "publisher"


# Output Keys  #################################################################
OUTPUT_RESPONSE_KEY = "response"


# helpers  #####################################################################


def _convert_filename_safe(original):
    return re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", original)


def _convert_keywords(entries):
    opt = []
    for e in entries:
        filename_safe = _convert_filename_safe(e)
        opt.append(re.sub(r"[ \.]", "_", filename_safe))

    return opt


def _add_party_entries(parties, prefix):
    cnt = len(parties)
    if cnt == 0:
        return []
    elif cnt == 1:
        entry = prefix + "=" + parties[0]
        return [entry]
    else:
        entry = prefix + "{" + SEP.join(parties) + "}"
        return [entry]


# formatter  ###################################################################


def _format_opus(extract, title, year, tags):  # ===============================

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
    safe_title = _convert_filename_safe(title)
    folder_name = "[{year}]{title}".format(year=year, title=safe_title)
    resource_name = folder_name + "{" + SEP.join(tags) + "}"

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

    return response


def _format_shelver(extract, title, year, tags):  # ============================

    # on parties  --------------------------------------------------------------
    # add authors
    parties = _convert_keywords(extract[EXTRACT_AUTHOR_KEY])

    # add editors
    editors = _convert_keywords(extract[EXTRACT_EDITOR_KEY])
    parties.extend(_add_party_entries(editors, "edr"))

    # add translators
    translators = _convert_keywords(extract[EXTRACT_TRANSLATOR_KEY])
    parties.extend(_add_party_entries(translators, "tr"))

    # on publisher  ------------------------------------------------------------
    publisher = extract[EXTRACT_PUBLISHER_KEY]

    # on tags  -----------------------------------------------------------------

    # format as response  ------------------------------------------------------

    response = """
Title Only:

```
{title}
```

Basic Info:

```
{title}[{year}]{parties}[{publisher}]
```

Full Info:

```
{title}[{year}]{parties}[{publisher}]{{{tags}}}
```

Multiple Lines:

```
{title}
[{year}]{parties}[{publisher}]{{
    {tags}
}}
```
""".format(
        title=_convert_filename_safe(title),
        year=year,
        parties=SEP.join(parties),
        publisher=publisher,
        tags=SEP.join(tags),
    )
    return response


# Entry Point  #################################################################
def main(extract: dict, target: str):
    """
    :param extract:
    :type extract: dict
    :param target: target/mode of operation, "Opus" or "Shelver"
    :type target: str
    :return: {
        "response": response formatted in md
    }
    :rtype: dict{"response": str}
    """

    title = extract[EXTRACT_TITLE_KEY]
    year = extract[EXTRACT_YEAR_KEY]
    tags = extract[EXTRACT_TAGS_KEY]

    response = (
        _format_opus(extract, title, year, tags)
        if target == "Opus"
        else _format_shelver(extract, title, year, tags)
    )
    return {OUTPUT_RESPONSE_KEY: response}
