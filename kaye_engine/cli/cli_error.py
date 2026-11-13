"""
cli_error.py

define ``fmt_unknown`` and ``report_unknown`` -- the one shape every
informational command gives a name no registry holds: ``unknown NOUN:
NAME``, plus the closest registered name when one is near
"""

import difflib

import kamilog

from kaye_engine import LOGGER_NAME

__all__ = ("fmt_unknown", "report_unknown")

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)


# Public API  ##################################################################
def fmt_unknown(noun, name, choices):
    """
    :param noun: what ``name`` should have named, the command's own name,
            e.g. ``"glossary"``
    :type noun: str
    :param name: the name the user gave
    :type name: str
    :param choices: every name the registry holds
    :type choices: collections.abc.Iterable[str]
    :return: ``unknown NOUN: NAME``, plus a ``did you mean`` line naming
            the closest choice when one is near
    :rtype: str
    """
    message = "unknown {}: {}".format(noun, name)
    close = difflib.get_close_matches(name, list(choices), n=1)
    if close:
        message += "\ndid you mean: {}".format(close[0])
    return message


def report_unknown(noun, name, choices):
    """
    log ``fmt_unknown`` as an error and leave with exit status 1


    :param noun: see :func:`fmt_unknown`
    :type noun: str
    :param name: see :func:`fmt_unknown`
    :type name: str
    :param choices: see :func:`fmt_unknown`
    :type choices: collections.abc.Iterable[str]
    :raises SystemExit: always
    """
    logger.error(fmt_unknown(noun, name, choices))
    raise SystemExit(1)
