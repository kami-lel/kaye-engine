"""
package_meta.py

define ``read_package_meta`` -- the manifest metadata of one consumer,
read from its own installed distribution
"""

from dataclasses import dataclass
from email.utils import parseaddr
from importlib.metadata import PackageNotFoundError, metadata

import kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME

__all__ = ("PackageMeta", "read_package_meta")

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)


@dataclass(frozen=True)
class PackageMeta:
    """
    summary, author and project URLs of an installed distribution
    """

    summary: str
    author_name: str
    author_email: str
    homepage: str
    repository: str


def read_package_meta(distribution_name):
    """
    :param distribution_name: installed distribution name, the
            canonical name of a consumer
    :type distribution_name: str
    :raises SystemExit: exit code 1, when the distribution is not
            installed
    :return: its manifest metadata
    :rtype: PackageMeta
    """
    try:
        meta = metadata(distribution_name)
    except PackageNotFoundError as err:
        logger.critical("package metadata not found:\t" + distribution_name)
        raise SystemExit(1) from err

    author_name, author_email = parseaddr(meta.get("Author-email") or "")
    urls = dict(
        _url.split(", ", 1) for _url in meta.get_all("Project-URL") or []
    )
    return PackageMeta(
        summary=meta["Summary"] or "",
        author_name=author_name,
        author_email=author_email,
        homepage=urls.get("homepage", ""),
        repository=urls.get("Repository", ""),
    )
