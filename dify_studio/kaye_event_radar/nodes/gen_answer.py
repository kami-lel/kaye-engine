from datetime import date as date_cls

EVENT_TEMPLATE = """## [{name}]({link})

- 🕒 **{time}**
- 💰 {price}
- 📍 {location}

{summary}

"""


def create_date_line(date):
    month_str, day_str = date.split("-")
    dt = date_cls(date_cls.today().year, int(month_str), int(day_str))
    weekday = dt.strftime("%a")
    return "# {weekday} {date}\n".format(weekday=weekday, date=date)


def main(event_search_result: dict):
    # tab by date  -------------------------------------------------------------
    by_dates = {}

    for event in event_search_result["events"]:
        date = event["date"]
        if date not in by_dates:
            by_dates[date] = []  # init a new list

        by_dates[date].append(event)

    # create md result  --------------------------------------------------------
    answer_parts = []

    for date, events_of_day in sorted(by_dates.items()):
        answer_parts.append(create_date_line(date))

        for event in events_of_day:
            answer_parts.append(EVENT_TEMPLATE.format(**event))

    opt = "".join(answer_parts)
    return {"output": opt}
