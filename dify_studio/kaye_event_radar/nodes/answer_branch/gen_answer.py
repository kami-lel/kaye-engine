from datetime import date as date_cls

EVENT_TEMPLATE = """## [{name}]({link})

- 🕒 **{time}**
- 💰 {price}
- 📍 {location}

{summary}

"""


def _filter_events(events, filtered_events_names):
    return events  # TODO


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
    # TODO doc
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
    create a standard, well-formatted answer in ``md``


    :param event_search_result:
    :type event_search_result: dict
    :return: ``opt`` is a ``str`` of well-formatted answer in ``md``
    """
    # TODO update doc

    filtered_events = _filter_events(events, filtered_events_names)
    opt = _generate_md_format(filtered_events)

    return {"output": opt}
