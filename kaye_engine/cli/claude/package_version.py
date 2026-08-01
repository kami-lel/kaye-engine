"""
package_version.py

define ``resolve_package_version``
"""

from importlib.metadata import PackageNotFoundError, version

from kaye_engine import PACKAGE_NAME, kamilog
from . import LOGGER_CLAUDE_NAME

__all__ = ("resolve_package_version",)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# entry point  #################################################################


def resolve_package_version():
    """
    :raises SystemExit: ``PACKAGE_NAME`` is not an installed distribution,
            e.g. running from an uninstalled source checkout
    :return: installed version of ``PACKAGE_NAME``
    :rtype: str
    """
    try:
        return version(PACKAGE_NAME)
    except PackageNotFoundError as err:
        logger.critical("package metadata not found:\t" + PACKAGE_NAME)
        raise SystemExit(1) from err
