"""
export_marketplace.py

define ``export_marketplace``
"""

from email.utils import parseaddr
from importlib.metadata import PackageNotFoundError, metadata
from pathlib import Path

from kaye_engine import PACKAGE_NAME, kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.plugin.export_folder import (
    export_plugin_as_folder,
)
from kaye_engine.cli.claude.plugin_marketplace_name import (
    get_marketplace_name,
    get_plugin_name,
)
from kaye_engine.cli.claude.setup import get_claude_cli_consumer_version

from .manifest import MarketplaceJson

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)


# constants  ###################################################################

_PLUGIN_CATEGORY = "productivity"


# Main Entry Point  ############################################################
def export_marketplace(marketplace_folder, *, surface=None):
    """
    export the Kaye plugin and write a marketplace manifest for it

    calls ``export_plugin_as_folder`` to write the plugin into
    ``<marketplace_folder>/plugins/<PLUGIN_NAME>/``, then writes
    ``.claude-plugin/marketplace.json`` at ``marketplace_folder`` listing
    the plugin with source ``"./plugins/<PLUGIN_NAME>"``


    :param marketplace_folder: directory to write the marketplace into
    :type marketplace_folder: Path-like
    :param surface: Claude surface(s) to checkmark affordances for,
            forwarded to :func:`export_plugin_as_folder`
    :type surface: ClaudeSurface, optional
    :return: path to the written marketplace.json
    :rtype: Path
    """
    marketplace_folder = Path(marketplace_folder)
    marketplace_name = get_marketplace_name()
    plugin_name = get_plugin_name()
    plugin_keywords = [
        "prompt-engineering",
        "persona",
        "agent",
        plugin_name,
    ]

    logger.debug("exporting plugin into marketplace folder")
    export_plugin_as_folder(marketplace_folder / "plugins", surface=surface)

    try:
        meta = metadata(PACKAGE_NAME)
    except PackageNotFoundError as err:
        logger.critical("package metadata not found:\t" + PACKAGE_NAME)
        raise SystemExit(1) from err
    pkg_version = get_claude_cli_consumer_version()

    pkg_author, pkg_author_email = parseaddr(meta.get("Author-email") or "")
    pkg_urls = dict(
        _url.split(", ", 1) for _url in meta.get_all("Project-URL") or []
    )
    pkg_homepage = pkg_urls.get("homepage", "")
    pkg_repository = pkg_urls.get("Repository", "")

    with MarketplaceJson(marketplace_folder) as market:
        market.name = marketplace_name
        market.description = meta["Summary"]
        market.version = pkg_version
        market.owner_name = pkg_author
        market.owner_email = pkg_author_email
        market.plugin_name = plugin_name
        market.plugin_source = "./plugins/" + plugin_name
        market.plugin_display_name = meta["Name"]
        market.plugin_description = meta["Summary"]
        market.plugin_version = pkg_version
        market.plugin_author_name = pkg_author
        market.plugin_author_email = pkg_author_email
        market.plugin_homepage = pkg_homepage
        market.plugin_repository = pkg_repository
        market.plugin_keywords = plugin_keywords
        market.plugin_category = _PLUGIN_CATEGORY

    logger.succ("write marketplace manifest:\t" + str(market.path))

    return market.path.resolve()
