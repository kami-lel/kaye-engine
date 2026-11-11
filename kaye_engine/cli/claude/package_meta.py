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

__all__ = ("PackageMeta", "get_plugin_keywords", "read_package_meta")

# keywords of a distribution naming none of its own
_DEFAULT_KEYWORDS = ("prompt-engineering", "agent")

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)


@dataclass(frozen=True)
class PackageMeta:
    """
    summary, author, project URLs and keywords of an installed
    distribution
    """

    version: str
    summary: str
    author_name: str
    author_email: str
    homepage: str
    repository: str
    keywords: tuple = ()


def get_plugin_keywords(meta, plugin_name):
    """
    :param meta: the distribution's metadata
    :type meta: PackageMeta
    :param plugin_name: canonical name of the consumer, always the last
            keyword
    :type plugin_name: str
    :return: the distribution's own keywords, else the generic defaults,
            then ``plugin_name``
    :rtype: list[str]
    """
    keywords = list(meta.keywords or _DEFAULT_KEYWORDS)
    if plugin_name not in keywords:
        keywords.append(plugin_name)
    return keywords


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
        version=meta["Version"] or "",
        summary=meta["Summary"] or "",
        author_name=author_name,
        author_email=author_email,
        homepage=urls.get("homepage", ""),
        repository=urls.get("Repository", ""),
        keywords=tuple(
            word.strip()
            for word in (meta.get("Keywords") or "").split(",")
            if word.strip()
        ),
    )
