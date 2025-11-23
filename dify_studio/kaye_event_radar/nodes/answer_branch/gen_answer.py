from datetime import date as date_cls

EVENT_TEMPLATE = """## [{name}]({link})

- 🕒 **{time}**
- 💰 {price}
- 📍 {location}

{summary}

"""


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


def _create_date_line(date):
    """
    :param date:
    :type date: datetime.date
    :return: a ``md`` heading line containing day-of-week and date
    :rtype: str
    """
    month_str, day_str = date.split("-")
    dt = date_cls(date_cls.today().year, int(month_str), int(day_str))
    weekday = dt.strftime("%a")
    return "# {weekday} {date}\n".format(weekday=weekday, date=date)


def _generate_md_format(events):
    """
    create a well-formatted ``md`` text

    :param events:
    :type events: list[dict]
    :return: formatted text
    :rtype: str
    """
    # tab by date  -------------------------------------------------------------
    by_dates = {}

    for event in events["events"]:
        date = event["date"]
        if date not in by_dates:
            by_dates[date] = []  # init a new list

        by_dates[date].append(event)

    # create md result  --------------------------------------------------------
    answer_parts = []

    for date, events_of_day in sorted(by_dates.items()):
        answer_parts.append(_create_date_line(date))

        for event in events_of_day:
            answer_parts.append(EVENT_TEMPLATE.format(**event))

    return "".join(answer_parts)


def main(events: list[dict], filtered_events_names: dict):
    """
    create a well-formatted ``md`` text answer of ``events`` after filtering


    :param events:
    :type events: list[dict]
    :param filtered_events_names:
    :type filtered_events_names: dict
    :return: ``opt`` is a ``str`` of well-formatted answer text in ``md``
    :rtype: dict
    """

    filtered_events = _filter_events(events, filtered_events_names)
    opt = _generate_md_format(filtered_events)

    return {"output": opt}
