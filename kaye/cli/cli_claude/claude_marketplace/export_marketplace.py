"""
export_marketplace.py

define ``export_marketplace``
"""

from importlib.metadata import metadata, version
from pathlib import Path

from kaye import logger
from kaye import PROGRAM_NAME
from kaye.cli.cli_claude.claude_plugin.export_plugin_as_folder import (
    export_plugin_as_folder,
)

from .marketplace_json import MarketplaceJson

# constants  ===================================================================

_PLUGIN_KEYWORDS = ["prompt-engineering", "persona", "agent", PROGRAM_NAME]
_PLUGIN_CATEGORY = "productivity"

# entry point  #################################################################


def export_marketplace(marketplace_folder):
    """
    export the Kaye plugin and write a marketplace manifest for it

    calls ``export_plugin_as_folder`` to write the plugin into
    ``<marketplace_folder>/<PROGRAM_NAME>/``, then writes
    ``.claude-plugin/marketplace.json`` at ``marketplace_folder`` listing
    the plugin with source ``"./<PROGRAM_NAME>"``


    :param marketplace_folder: directory to write the marketplace into
    :type marketplace_folder: Path-like
    :return: path to the written marketplace.json
    :rtype: Path
    """
    marketplace_folder = Path(marketplace_folder)

    logger.debug("exporting plugin into marketplace folder")
    export_plugin_as_folder(marketplace_folder)

    meta = metadata(PROGRAM_NAME)
    pkg_version = version(PROGRAM_NAME)
    pkg_author = meta["Author"] or ""
    pkg_author_email = meta.get("Author-Email") or ""
    pkg_homepage = meta.get("Home-Page") or ""
    pkg_repository = (
        meta.get("Project-URL", "").split(", ")[-1]
        if meta.get("Project-URL")
        else ""
    )

    with MarketplaceJson(marketplace_folder) as market:
        market.name = PROGRAM_NAME
        market.description = meta["Summary"]
        market.version = pkg_version
        market.owner_name = pkg_author
        market.owner_email = pkg_author_email
        market.plugin_name = PROGRAM_NAME
        market.plugin_source = "./" + PROGRAM_NAME
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

    return market.path
