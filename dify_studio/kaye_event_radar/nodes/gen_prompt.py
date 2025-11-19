def main(prompt_event_search: str, interested_topics: list[str]):
    lines = ["#### Interested Topics", ""]

    for topic in interested_topics:
        lines.append(topic)

    opt = prompt_event_search.format(INTERESTED_TOPICS="\n".join(lines))
    return {"output": opt}
