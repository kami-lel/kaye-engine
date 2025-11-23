from datetime import timedelta, date as date_cls

EVENTBRITE_URL = "https://www.eventbrite.com/d/ca--los-angeles/all-events/?page=1&start_date={}&end_date={}"
EVENTBRITE_DATE = "%Y-%m-%d"
DOWNTOWN_LA_URL = "https://downtownla.com/calendar#{}-to-{}"
DOWNTOWN_LA_DATE = "%m-%d-%y"
LA_LIVE_URL = "https://www.lalive.com/events/filter/{}/{}/"
LA_LIVE_DATE = "%Y-%m-%d"
DISCOVER_LA_URL = "https://www.discoverlosangeles.com/events"


def _create_date_range():
    """
    create a date range starting **today**, and ending on **coming Sunday**,
    spanning for at max 1 week


    :return: start & end date
    :rtype: tuple(datetime.date, datetime.date)
    """
    start_date = date_cls.today()

    # find coming Sunday
    days_ahead = ((6 - start_date.weekday()) % 7) or 7
    end_date = start_date + timedelta(days=days_ahead)

    return start_date, end_date


def main():
    """
    dynamically create information for scarping various websites


    :return: ``opt`` is a ``list`` of urls (``str``) to be scraped
    """

    start_date, end_date = _create_date_range()

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
    opt.append(DISCOVER_LA_URL)

    # LA Live.com
    opt.append(
        LA_LIVE_URL.format(
            start_date.strftime(LA_LIVE_DATE),
            end_date.strftime(LA_LIVE_DATE),
        )
    )

    # return all urls  ---------------------------------------------------------
    return {"output": opt}
