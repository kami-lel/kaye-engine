def main(event_search_prompt: str, interested_topics: list[str]):
    """
    generate ``event_search_prompt`` as a full, usable prompt
    by populated it of ``interested_topics``


    :param event_search_prompt:
    :type event_search_prompt: str
    :param interested_topics:
    :type interested_topics: list[str]
    :return: ``opt`` is the populated, usable prompt (typed ``str`` )
    """
    lines = ["#### Interested Topics", ""]

    for topic in interested_topics:
        lines.append(topic)

    opt = event_search_prompt.format(INTERESTED_TOPICS="\n".join(lines))
    return {"output": opt}
