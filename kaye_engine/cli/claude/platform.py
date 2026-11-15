"""
platform.py

define ``ClaudePlatform``, ``CLAUDE_PLATFORM`` -- the Claude
``PluginPlatform``: ``.claude-plugin/plugin.json`` and
``.claude-plugin/marketplace.json``
"""

from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.marketplace.manifest import (
    MarketplaceJson,
    MarketplacePlugin,
)
from kaye_engine.cli.claude.plugin.manifest import ManifestPluginJson
from kaye_engine.cli.plugin_platform.package_meta import get_plugin_keywords
from kaye_engine.cli.plugin_platform.platform import PluginPlatform

__all__ = ("CLAUDE_PLATFORM", "ClaudePlatform")

# constants  ###################################################################

_PLUGIN_CATEGORY = "productivity"


class ClaudePlatform(PluginPlatform):  #########################################
    """
    the Anthropic Claude plugin platform
    """

    name = "claude"
    default_surface = ("claude",)
    logger_name = LOGGER_CLAUDE_NAME

    def write_plugin_manifest(self, plugin_root, consumer, meta):
        plugin_name = consumer.canonical_name
        with ManifestPluginJson(plugin_root) as manifest:
            manifest.name = plugin_name
            manifest.display_name = consumer.display_name
            manifest.version = consumer.version
            manifest.description = meta.summary
            manifest.author_name = meta.author_name
            manifest.author_email = meta.author_email
            manifest.homepage = meta.homepage
            manifest.repository = meta.repository
            manifest.keywords = get_plugin_keywords(meta, plugin_name)

    def build_marketplace_entry(self, consumer, meta, source):
        return MarketplacePlugin(
            name=consumer.canonical_name,
            source=source,
            display_name=consumer.display_name,
            description=meta.summary,
            version=consumer.version,
            author_name=meta.author_name,
            author_email=meta.author_email,
            homepage=meta.homepage,
            repository=meta.repository,
            keywords=get_plugin_keywords(meta, consumer.canonical_name),
            category=_PLUGIN_CATEGORY,
        )

    def write_marketplace_manifest(self, root, name, entries, engine_meta):
        with MarketplaceJson(root) as market:
            market.name = name
            market.description = engine_meta.summary
            market.version = engine_meta.version
            market.owner_name = engine_meta.author_name
            market.owner_email = engine_meta.author_email
            market.plugins = list(entries)
        return market.path.resolve()


# the one Claude platform instance every exporter shares
CLAUDE_PLATFORM = ClaudePlatform()
