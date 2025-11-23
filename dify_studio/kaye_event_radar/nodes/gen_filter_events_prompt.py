def main(filter_events_prompt: str, interested_topics: list[str]):
    """
    generate ``filter_events_prompt`` as a full, usable prompt
    by populated it of ``interested_topics``


    :param filter_events_prompt:
    :type filter_events_prompt: str
    :param interested_topics:
    :type interested_topics: list[str]
    :return: ``opt`` is the populated, usable prompt (typed ``str``)
    """
    lines = ["#### Interested Topics", ""]

    for topic in interested_topics:
        lines.append(topic)

    opt = filter_events_prompt.format(INTERESTED_TOPICS="\n".join(lines))
    return {"output": opt}
