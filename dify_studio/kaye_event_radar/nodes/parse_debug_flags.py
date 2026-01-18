"""
parse ``debug_flags`` as bitwise flags, assume integer:

- 1: ``skip_event_filtering``
- 2: ``use_example_events``
- 4: ``only_print_urls`` during scraping mode


:param debug_flags:
:type debug_flags: float
:return: entries with key as flag names (v.s.) and value as ``bool``
:rtype: dict{str: bool}
"""


def main(debug_flags: float):  # pylint: disable=missing-function-docstring
    flags = int(debug_flags)

    skip_event_filtering = bool(flags & 1)
    use_example_events = bool(flags & 2)
    only_print_urls = bool(flags & 4)

    return {
        "skip_event_filtering": skip_event_filtering,
        "use_example_events": use_example_events,
        "only_print_urls": only_print_urls,
    }
