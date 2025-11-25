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
    create a date range starting **today**, and ending on **next Sunday**

    *next Sunday* is:

    - if weekend (Sat, Sun): next next Sunday
    - else: coming Sunday


    :return: start date, end date, days count (inclusive)
    :rtype: tuple(datetime.date, datetime.date, int)
    """
    start_date = date_cls.today()

    day_of_week = start_date.weekday()
    if day_of_week >= 5:  # weekend: Sat,Sun
        days_passed = 13 - day_of_week
    else:
        days_passed = 6 - day_of_week

    end_date = start_date + timedelta(days=days_passed)

    return start_date, end_date, days_passed + 1


def main(
    enable_eventbride,
    enable_downtown_la,
    enable_discover_la,
    enable_la_live,
    enable_usc_event_calendar,
    enable_engage_sc,
):
    """
    dynamically create information for scarping various websites


    :return: ``opt`` is a ``list`` of urls (``str``) to be scraped
    """
    start_date, end_date, days_cnt = _create_date_range()

    # create urls  -------------------------------------------------------------
    opt = []

    # eventide
    if enable_eventbride:
        opt.append(
            EVENTBRITE_URL.format(
                start_date.strftime(EVENTBRITE_DATE),
                end_date.strftime(EVENTBRITE_DATE),
            )
        )

    # downtownla.com
    if False and enable_downtown_la:
        opt.append(
            DOWNTOWN_LA_URL.format(
                start_date.strftime(DOWNTOWN_LA_DATE),
                end_date.strftime(DOWNTOWN_LA_DATE),
            )
        )

    # Discover LA
    if enable_discover_la:
        opt.append(DISCOVER_LA_URL)

    # LA Live.com
    if enable_la_live:
        opt.append(
            LA_LIVE_URL.format(
                start_date.strftime(LA_LIVE_DATE),
                end_date.strftime(LA_LIVE_DATE),
            )
        )

    # USC Event Calendar
    if enable_usc_event_calendar:
        opt.append(
            USC_EVENT_CALENDAR_URL.format(
                start_date.strftime(USC_EVENT_CALENDAR_DATE), days_cnt
            )
        )

    # engageSC
    if enable_engage_sc:
        opt.append(
            ENGAGE_SC_URL.format(
                start_date.strftime(ENGAGE_SC_DATE),
                end_date.strftime(ENGAGE_SC_DATE),
            )
        )

    # bug spider.web fail to extract full info via only url

    # return all urls  ---------------------------------------------------------
    return {"output": opt}
