"""
consumer.py

define ``register_consumer`` and the getters of the registered identity
"""

import re

import kamilog
from kaye_engine import LOGGER_NAME

__all__ = (
    "get_consumer_canonical_name",
    "get_consumer_display_name",
    "get_consumer_version",
    "register_consumer",
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################

_KEBAB_PATTERN = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")

# registered identity of the consumer project
_display_name = None
_canonical_name = None
_version = None


# Public API  ##################################################################


def register_consumer(display_name, canonical_name, version):
    """
    register the consumer project's identity; the single source every CLI
    subcommand derives its names and version from

    Repeated calls overwrite the previous registration


    :param display_name: human-readable name of the consumer project
    :type display_name: str
    :param canonical_name: kebab-case machine name of the consumer project
    :type canonical_name: str
    :param version: version string of the consumer project
    :type version: str
    :raises ValueError: when an arg is not a non-empty string, or
            ``canonical_name`` is not kebab case
    """
    global _display_name, _canonical_name, _version  # pylint: disable=W0603

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

    _display_name = display_name
    _canonical_name = canonical_name
    _version = version


def _get_registered(val, description):
    """
    :raises SystemExit: exit code 1, when ``val`` is still unset
    :return: ``val``
    """
    if val is None:
        logger.critical(
            "no consumer %s set\n"
            "a consumer project should call "
            "register_consumer(...) before invoking this CLI",
            description,
        )
        raise SystemExit(1)
    return val


def get_consumer_display_name():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``register_consumer(...)``
    :return: registered display name
    :rtype: str
    """
    return _get_registered(_display_name, "display name")


def get_consumer_canonical_name():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``register_consumer(...)``
    :return: registered canonical (kebab case) name
    :rtype: str
    """
    return _get_registered(_canonical_name, "canonical name")


def get_consumer_version():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``register_consumer(...)``
    :return: registered version string
    :rtype: str
    """
    return _get_registered(_version, "version")
