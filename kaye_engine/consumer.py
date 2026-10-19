"""
consumer.py

define ``Consumer``, ``register_consumer``, ``set_entry_consumer``, and
the getters of the registered consumers -- any number of consumer
packages may share one process, each registering its own record; the
setup a console command runs names one of them the entry consumer
"""

import re
from dataclasses import dataclass

import kamilog
from kaye_engine import LOGGER_NAME

__all__ = (
    "Consumer",
    "check_consumer",
    "get_consumer",
    "get_consumer_canonical_name",
    "get_consumer_display_name",
    "get_consumer_version",
    "get_entry_consumer",
    "iter_consumers",
    "register_consumer",
    "set_entry_consumer",
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################

_KEBAB_PATTERN = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")


@dataclass(frozen=True)
class Consumer:
    """
    identity of one consumer package


    :param display_name: human-readable name of the consumer
    :type display_name: str
    :param canonical_name: kebab-case machine name of the consumer, also
            the name of its installed distribution and of its plugin
    :type canonical_name: str
    :param version: version string of the consumer
    :type version: str
    """

    display_name: str
    canonical_name: str
    version: str


# registered consumers, by canonical name, in registration order
_consumers = {}

# canonical name of the consumer owning the process-wide CLI identity
_entry_canonical_name = None


# Public API  ##################################################################


def register_consumer(display_name, canonical_name, version):
    """
    add one consumer record; each package registers its own


    :param display_name: human-readable name of the consumer
    :type display_name: str
    :param canonical_name: kebab-case machine name of the consumer
    :type canonical_name: str
    :param version: version string of the consumer
    :type version: str
    :raises ValueError: when an arg is not a non-empty string,
            ``canonical_name`` is not kebab case, or is already registered
    :return: the registered record
    :rtype: Consumer
    """
    for arg_name, val in (
        ("display_name", display_name),
        ("canonical_name", canonical_name),
        ("version", version),
    ):
        if not isinstance(val, str) or not val.strip():
            raise ValueError("{} must be a non-empty str".format(arg_name))
    if not _KEBAB_PATTERN.fullmatch(canonical_name):
        raise ValueError(
            "canonical_name must be kebab case, got {!r}".format(
                canonical_name
            )
        )
    if canonical_name in _consumers:
        raise ValueError(
            "duplicate consumer canonical name: {}".format(canonical_name)
        )

    record = Consumer(display_name, canonical_name, version)
    _consumers[canonical_name] = record
    return record


def check_consumer(canonical_name):
    """
    :param canonical_name: consumer an exportable names
    :type canonical_name: str
    :raises ValueError: no consumer is registered under ``canonical_name``
    :return: ``canonical_name``, unchanged
    :rtype: str
    """
    if canonical_name not in _consumers:
        raise ValueError(
            "unregistered consumer {!r}; call register_consumer(...) "
            "first".format(canonical_name)
        )
    return canonical_name


def get_consumer(canonical_name):
    """
    :raises ValueError: no consumer is registered under ``canonical_name``
    :return: the record registered under ``canonical_name``
    :rtype: Consumer
    """
    return _consumers[check_consumer(canonical_name)]


def iter_consumers():
    """
    :return: every registered consumer, in registration order
    :rtype: tuple[Consumer, ...]
    """
    return tuple(_consumers.values())


def set_entry_consumer(canonical_name):
    """
    name the consumer owning the process-wide CLI identity, the one every
    ``get_consumer_*`` getter reads; called once, by the setup a console
    command runs, so a later call wins


    :param canonical_name: a registered consumer
    :type canonical_name: str
    :raises ValueError: no consumer is registered under ``canonical_name``
    """
    global _entry_canonical_name  # pylint: disable=global-statement

    _entry_canonical_name = check_consumer(canonical_name)


def get_entry_consumer():
    """
    :raises SystemExit: exit code 1, when no entry consumer is set
    :return: the entry consumer's record
    :rtype: Consumer
    """
    if _entry_canonical_name is None:
        logger.critical(
            "no entry consumer set\n"
            "a consumer project should call register_consumer(...) and "
            "set_entry_consumer(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return _consumers[_entry_canonical_name]


def get_consumer_display_name():
    """
    :raises SystemExit: exit code 1, when no entry consumer is set
    :return: the entry consumer's display name
    :rtype: str
    """
    return get_entry_consumer().display_name


def get_consumer_canonical_name():
    """
    :raises SystemExit: exit code 1, when no entry consumer is set
    :return: the entry consumer's canonical (kebab case) name
    :rtype: str
    """
    return get_entry_consumer().canonical_name


def get_consumer_version():
    """
    :raises SystemExit: exit code 1, when no entry consumer is set
    :return: the entry consumer's version string
    :rtype: str
    """
    return get_entry_consumer().version


def _clear_consumers():
    """
    drop every consumer and the entry consumer, for tests
    """
    global _entry_canonical_name  # pylint: disable=global-statement

    _consumers.clear()
    _entry_canonical_name = None
