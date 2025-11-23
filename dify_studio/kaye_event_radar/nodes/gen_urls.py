from datetime import timedelta, date as date_cls

EVENTBRITE_URL = (
    "https://www.eventbrite.com/d/ca--los-angeles/all-events/"
    "?page=1&start_date={}&end_date={}"
)
EVENTBRITE_DATE = "%Y-%m-%d"

DOWNTOWN_LA_URL = "https://downtownla.com/calendar#{}-to-{}"
DOWNTOWN_LA_DATE = "%m-%d-%y"

LA_LIVE_URL = "https://www.lalive.com/events/filter/{}/{}/"
LA_LIVE_DATE = "%Y-%m-%d"

DISCOVER_LA_URL = "https://www.discoverlosangeles.com/events"

USC_EVENT_CALENDAR_URL = (
    "https://calendar.usc.edu/calendar/day/"
    "{}?card_size=small&order=date&days={}&experience="
)
USC_EVENT_CALENDAR_DATE = "%Y/%m/%d"

ENGAGE_SC_URL = "https://engage.usc.edu/events?from_date={}&to_date={}"
ENGAGE_SC_DATE = "%d+%b+%Y"


def _create_date_range():
    """
    create a date range starting **today**, and ending on **coming Sunday**,
    spanning for at max 1 week


    :return: start date, end date, days count (inclusive)
    :rtype: tuple(datetime.date, datetime.date)
    """
    start_date = date_cls.today()

    # Fixme when weekend (Fri, Sat, Sun, find coming week)
    # BUG inclusive days count
    # find coming Sunday
    days_cnt = ((6 - start_date.weekday()) % 7) or 7
    end_date = start_date + timedelta(days=days_cnt)

    return start_date, end_date, days_cnt


def main():
    """
    dynamically create information for scarping various websites


    :return: ``opt`` is a ``list`` of urls (``str``) to be scraped
    """
    start_date, end_date, days_cnt = _create_date_range()

    # create urls  -------------------------------------------------------------
    opt = []

    # eventide
    # Fixme only search 1st page
    opt.append(
        EVENTBRITE_URL.format(
            start_date.strftime(EVENTBRITE_DATE),
            end_date.strftime(EVENTBRITE_DATE),
        )
    )

    # downtownla.com
    opt.append(
        DOWNTOWN_LA_URL.format(
            start_date.strftime(DOWNTOWN_LA_DATE),
            end_date.strftime(DOWNTOWN_LA_DATE),
        )
    )

    # Discover LA
    # Fixme no date filter
    opt.append(DISCOVER_LA_URL)

    # LA Live.com
    # Bug filter not applied
    opt.append(
        LA_LIVE_URL.format(
            start_date.strftime(LA_LIVE_DATE),
            end_date.strftime(LA_LIVE_DATE),
        )
    )

    # USC Event Calendar
    # Fixme only page 1
    opt.append(
        USC_EVENT_CALENDAR_URL.format(
            start_date.strftime(USC_EVENT_CALENDAR_DATE), days_cnt
        )
    )

    # engageSC
    opt.append(
        ENGAGE_SC_URL.format(
            start_date.strftime(ENGAGE_SC_DATE),
            end_date.strftime(ENGAGE_SC_DATE),
        )
    )

    # return all urls  ---------------------------------------------------------
    return {"output": opt}
