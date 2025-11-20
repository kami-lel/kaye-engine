def main(prompt_events_search: str, interested_topics: list[str]):
    lines = ["#### Interested Topics", ""]

    for topic in interested_topics:
        lines.append(topic)

    opt = prompt_events_search.format(INTERESTED_TOPICS="\n".join(lines))
    return {"output": opt}
