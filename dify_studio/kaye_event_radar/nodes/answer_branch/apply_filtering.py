def _filter_events(events, filtered_events_names):
    """
    :param events:
    :type events: list[dict]
    :param filtered_events_names:
    :type filtered_events_names: list[str]
    :return: filter ``events``
            by keep only those with names appeared in ``filtered_events_names``
    :rtype: list[dict]
    """
    return [
        event for event in events if event["name"] in filtered_events_names
    ]


def main(
    events: list[dict], filtered_events_names: dict, debug_skip_event_filtering
):
    """
    filter ``events`` by selecting only those names appeared in ``names``


    :param events:
    :type events: list[dict]
    :param names:
    :type names: list[str]
    :param debug_skip_event_filtering:
    :type debug_skip_event_filtering: bool
    :return: ``opt`` is filtered events, (identical structure as ``events``)
    """
    if debug_skip_event_filtering:
        opt = events
    else:
        opt = [
            event for event in events if event["name"] in filtered_events_names
        ]

    return {"output": opt}
