from datetime import date as date_cls

EVENT_TEMPLATE = """## [{name}]({link})

- 🕒 `{time}`
- 💰 {price}
- 📍 <ins>{location}</ins>

{summary}

"""


WARNING_TEMPLATE = """
<span style="color: red; font-weight: bold;">WARN : {}</span>
"""

DEBUG_SKIP_EVENT_FILTERING_WARNING = WARNING_TEMPLATE.format(
    "skip event filtering"
)
DEBUG_USE_EXAMPLE_EVENTS_WARNING = WARNING_TEMPLATE.format(
    "use example events"
)


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


def main(
    filtered_events: list[dict],
    debug_skip_event_filtering: float,
    debug_use_example_events_warning: float,
):
    """
    create a well-formatted ``md`` text answer of ``filtered_events``

    :param filtered_events:
    :type filtered_events: list[dict]
    :return: ``opt`` is the formatted text answer (typed ``str``)
    """

    # tab by date  -------------------------------------------------------------
    by_dates = {}

    for event in filtered_events:
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

    # warning for enabled debug flags
    if debug_skip_event_filtering:
        answer_parts.append(DEBUG_SKIP_EVENT_FILTERING_WARNING)
    if debug_use_example_events_warning:
        answer_parts.append(DEBUG_USE_EXAMPLE_EVENTS_WARNING)

    opt = "".join(answer_parts)
    return {"output": opt}
