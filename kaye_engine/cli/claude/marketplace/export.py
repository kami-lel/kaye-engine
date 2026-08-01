"""
export_marketplace.py

define ``export_marketplace``
"""

from email.utils import parseaddr
from importlib.metadata import metadata, version
from pathlib import Path

from kaye_engine import PACKAGE_NAME, kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME, PLUGIN_MARKETPLACE_NAME
from kaye_engine.cli.claude.plugin.export_folder import (
    export_plugin_as_folder,
)

from .manifest import MarketplaceJson

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# constants  ===================================================================

_PLUGIN_KEYWORDS = [
    "prompt-engineering",
    "persona",
    "agent",
    PLUGIN_MARKETPLACE_NAME,
]
_PLUGIN_CATEGORY = "productivity"

# entry point  #################################################################


def export_marketplace(marketplace_folder):
    """
    export the Kaye plugin and write a marketplace manifest for it

    calls ``export_plugin_as_folder`` to write the plugin into
    ``<marketplace_folder>/plugins/<PLUGIN_MARKETPLACE_NAME>/``, then writes
    ``.claude-plugin/marketplace.json`` at ``marketplace_folder`` listing
    the plugin with source ``"./plugins/<PLUGIN_MARKETPLACE_NAME>"``


    :param marketplace_folder: directory to write the marketplace into
    :type marketplace_folder: Path-like
    :return: path to the written marketplace.json
    :rtype: Path
    """
    marketplace_folder = Path(marketplace_folder)

    logger.debug("exporting plugin into marketplace folder")
    export_plugin_as_folder(marketplace_folder / "plugins")

    # FIXME Utilize kamilog here
    meta = metadata(PACKAGE_NAME)
    pkg_version = version(PACKAGE_NAME)
    pkg_author, pkg_author_email = parseaddr(meta.get("Author-email") or "")
    pkg_urls = dict(
        _url.split(", ", 1) for _url in meta.get_all("Project-URL") or []
    )
    pkg_homepage = pkg_urls.get("homepage", "")
    pkg_repository = pkg_urls.get("Repository", "")

    with MarketplaceJson(marketplace_folder) as market:
        market.name = PLUGIN_MARKETPLACE_NAME
        market.description = meta["Summary"]
        market.version = pkg_version
        market.owner_name = pkg_author
        market.owner_email = pkg_author_email
        market.plugin_name = PLUGIN_MARKETPLACE_NAME
        market.plugin_source = "./plugins/" + PLUGIN_MARKETPLACE_NAME
        market.plugin_display_name = meta["Name"]
        market.plugin_description = meta["Summary"]
        market.plugin_version = pkg_version
        market.plugin_author_name = pkg_author
        market.plugin_author_email = pkg_author_email
        market.plugin_homepage = pkg_homepage
        market.plugin_repository = pkg_repository
        market.plugin_keywords = _PLUGIN_KEYWORDS
        market.plugin_category = _PLUGIN_CATEGORY

    logger.succ("write marketplace manifest:\t" + str(market.path))

    return market.path.resolve()
