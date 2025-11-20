NAME_KEY = "name"
DATE_KEY = "date"
TIME_KEY = "time"
LOCATION_KEY = "location"
LINK_KEY = "link"
SUMMARY_KEY = "summary"
KEYWORDS_KEY = "keywords"


def main(event_search_result: dict):
    # tab by date  -------------------------------------------------------------
    by_dates = {}

    for event in event_search_result["events"]:
        date = event[DATE_KEY]
        entry = (
            event[NAME_KEY],
            event[TIME_KEY],
            event[LOCATION_KEY],
            event[LINK_KEY],
            event[SUMMARY_KEY],
            event[KEYWORDS_KEY],
        )
        if date not in by_dates:
            by_dates[date] = []  # init a new list

        by_dates[date].append(entry)

    # create md result  --------------------------------------------------------
    lines = []
    lines.append("# Events Radar")

    for date, events_of_day in sorted(by_dates.items()):
        lines.append("## {}".format(date))

        for name, time, location, link, summary, keywords in events_of_day:
            lines.append("### [{}]({})".format(name, link))
            lines.extend(["", summary, "", ""])
            lines.append("- {} {}".format(date, time))
            lines.append("- {}".format(location))
            lines.append("- {}".format(",".join(keywords)))

    opt = "\n".join(lines)
    return {"output": opt}
