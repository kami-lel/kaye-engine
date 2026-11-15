"""
repo.py

define ``set_repo_name``, ``set_repo_version`` and their getters -- the
repo a console command ships from, which names every release asset; the
setup a console command runs registers both, so a later call wins
"""

import re

import kamilog
from kaye_engine import LOGGER_NAME

__all__ = (
    "get_repo_name",
    "get_repo_version",
    "set_repo_name",
    "set_repo_version",
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################

_KEBAB_PATTERN = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")

# registered repo name and version, None until set
_repo_name = None
_repo_version = None


# Public API  ##################################################################


def set_repo_name(name):
    """
    name the repo the process ships from; a later call wins


    :param name: kebab-case repo name
    :type name: str
    :raises ValueError: when ``name`` is not a kebab-case str
    """
    global _repo_name  # pylint: disable=global-statement

    if not isinstance(name, str) or not _KEBAB_PATTERN.fullmatch(name):
        raise ValueError("repo name must be kebab case, got {!r}".format(name))
    _repo_name = name


def set_repo_version(version):
    """
    record the version of the repo the process ships from; a later call
    wins


    :param version: the repo's own version string
    :type version: str
    :raises ValueError: when ``version`` is not a non-empty str
    """
    global _repo_version  # pylint: disable=global-statement

    if not isinstance(version, str) or not version.strip():
        raise ValueError("repo version must be a non-empty str")
    _repo_version = version


def get_repo_name():
    """
    :raises SystemExit: exit code 1, when no repo name is set
    :return: the registered repo name
    :rtype: str
    """
    if _repo_name is None:
        logger.critical(
            "no repo name set\n"
            "a consumer project should call set_repo_name(...) before "
            "invoking this CLI"
        )
        raise SystemExit(1)
    return _repo_name


def get_repo_version():
    """
    :raises SystemExit: exit code 1, when no repo version is set
    :return: the registered repo version
    :rtype: str
    """
    if _repo_version is None:
        logger.critical(
            "no repo version set\n"
            "a consumer project should call set_repo_version(...) before "
            "invoking this CLI"
        )
        raise SystemExit(1)
    return _repo_version


def _clear_repo():
    """
    drop the repo name and version, for tests
    """
    global _repo_name, _repo_version  # pylint: disable=global-statement

    _repo_name = None
    _repo_version = None
