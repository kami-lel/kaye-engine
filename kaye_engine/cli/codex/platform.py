"""
platform.py

define ``CodexPlatform``, ``CODEX_PLATFORM`` -- the OpenAI Codex
``PluginPlatform``: root ``plugin.json`` plus ``.codex-plugin/plugin.json``,
and ``.agents/plugins/marketplace.json``
"""

import kamilog
from kaye_engine.cli.codex import LOGGER_CODEX_NAME
from kaye_engine.cli.codex.marketplace.manifest import (
    CodexMarketplace,
    CodexMarketplacePlugin,
)
from kaye_engine.cli.codex.plugin.manifest import CodexPluginManifest
from kaye_engine.cli.plugin_platform.package_meta import get_plugin_keywords
from kaye_engine.cli.plugin_platform.platform import PluginPlatform

__all__ = ("CODEX_PLATFORM", "CodexPlatform", "get_marketplace_display_name")

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CODEX_NAME)


class CodexPlatform(PluginPlatform):  ##########################################
    """
    the OpenAI Codex plugin platform
    """

    name = "codex"
    default_surface = ("codex",)
    logger_name = LOGGER_CODEX_NAME

    def write_plugin_manifest(self, plugin_root, consumer, meta):
        plugin_name = consumer.canonical_name
        CodexPluginManifest(
            name=plugin_name,
            version=consumer.version,
            description=meta.summary,
            display_name=consumer.display_name,
            author_name=meta.author_name,
            author_email=meta.author_email,
            homepage=meta.homepage,
            repository=meta.repository,
            keywords=get_plugin_keywords(meta, plugin_name),
        ).write(logger, plugin_root)

    def build_marketplace_entry(self, consumer, meta, source):
        return CodexMarketplacePlugin(name=consumer.canonical_name, path=source)

    def write_marketplace_manifest(self, root, name, entries, engine_meta):
        return CodexMarketplace(
            name=name,
            display_name=get_marketplace_display_name(name),
            plugins=list(entries),
        ).write(logger, root)


def get_marketplace_display_name(name):
    """
    :param name: kebab-case marketplace name, eg ``kaye-library``
    :type name: str
    :return: its title-case display name, eg ``Kaye Engine``
    :rtype: str
    """
    return " ".join(word.capitalize() for word in name.split("-"))


# the one Codex platform instance every exporter shares
CODEX_PLATFORM = CodexPlatform()
