"""
export_marketplace.py

define ``export_marketplace``
"""

from pathlib import Path

import kamilog
from kaye_engine import PACKAGE_NAME
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.package_meta import read_package_meta
from kaye_engine.cli.claude.plugin.export_folder import (
    export_plugin_as_folder,
)
from kaye_engine.cli.claude.plugin_marketplace_name import (
    get_marketplace_name,
    get_plugin_consumers,
)

from .manifest import MarketplaceJson, MarketplacePlugin

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)


# constants  ###################################################################

_PLUGIN_CATEGORY = "productivity"


# Main Entry Point  ############################################################
def export_marketplace(marketplace_folder, *, render_profile=None):
    """
    export every consumer's plugin and write the marketplace manifest
    listing them

    writes each plugin into ``<marketplace_folder>/plugins/<consumer>/``,
    then ``.claude-plugin/marketplace.json`` at ``marketplace_folder``,
    named after the engine and listing one plugin per consumer with source
    ``"./plugins/<consumer>"``; the whole marketplace is written from this
    process's consumers, so the last export wins


    :param marketplace_folder: directory to write the marketplace into
    :type marketplace_folder: Path-like
    :param render_profile: render options forwarded to
            :func:`export_plugin_as_folder`
    :type render_profile: RenderProfile, optional
    :return: path to the written marketplace.json
    :rtype: Path
    """
    marketplace_folder = Path(marketplace_folder)
    consumers = get_plugin_consumers()

    plugins = []
    for consumer in consumers:
        logger.debug("exporting plugin into marketplace: " + consumer.canonical_name)
        export_plugin_as_folder(
            marketplace_folder / "plugins",
            consumer,
            render_profile=render_profile,
        )
        meta = read_package_meta(consumer.canonical_name)
        plugins.append(
            MarketplacePlugin(
                name=consumer.canonical_name,
                source="./plugins/" + consumer.canonical_name,
                display_name=consumer.display_name,
                description=meta.summary,
                version=consumer.version,
                author_name=meta.author_name,
                author_email=meta.author_email,
                homepage=meta.homepage,
                repository=meta.repository,
                keywords=[
                    "prompt-engineering",
                    "persona",
                    "agent",
                    consumer.canonical_name,
                ],
                category=_PLUGIN_CATEGORY,
            )
        )

    engine_meta = read_package_meta(PACKAGE_NAME)
    with MarketplaceJson(marketplace_folder) as market:
        market.name = get_marketplace_name()
        market.description = engine_meta.summary
        market.owner_name = engine_meta.author_name
        market.owner_email = engine_meta.author_email
        market.plugins = plugins

    return market.path.resolve()
