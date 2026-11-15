"""
platform.py

define ``PluginPlatform`` -- the Strategy every plugin platform (Claude,
Codex) implements, so one template exporter writes plugins and
marketplaces for each
"""

from abc import ABC, abstractmethod

__all__ = ("PluginPlatform",)


class PluginPlatform(ABC):  ####################################################
    """
    what differs between plugin platforms: manifest files, marketplace
    file and entry shape, default render surface, reporting logger

    the template exporters in :mod:`kaye_engine.cli.plugin_platform.export`
    drive the shared steps and call these hooks; a platform holds no state
    beyond its constants


    :cvar name: platform name, eg ``claude``
    :cvar default_surface: render profile names a platform renders for
            unless the caller passes one
    :cvar logger_name: logger every exporter step reports through
    """

    name = ""
    default_surface = ()
    logger_name = ""

    @abstractmethod
    def write_plugin_manifest(self, plugin_root, consumer, meta):
        """
        write the plugin manifest file(s) of one consumer's plugin


        :param plugin_root: the plugin's own folder
        :type plugin_root: Path
        :param consumer: the consumer the plugin belongs to
        :type consumer: Consumer
        :param meta: the consumer distribution's metadata
        :type meta: PackageMeta
        """

    @abstractmethod
    def build_marketplace_entry(self, consumer, meta, source):
        """
        :param consumer: the consumer the listed plugin belongs to
        :type consumer: Consumer
        :param meta: the consumer distribution's metadata
        :type meta: PackageMeta
        :param source: the plugin folder, relative to the marketplace
                root, ``./`` prefixed
        :type source: str
        :return: one marketplace entry, handed back to
                :meth:`write_marketplace_manifest`
        """

    @abstractmethod
    def write_marketplace_manifest(self, root, name, entries, engine_meta):
        """
        write the marketplace manifest listing ``entries`` under ``root``


        :param root: the marketplace root folder
        :type root: Path
        :param name: marketplace name
        :type name: str
        :param entries: every entry :meth:`build_marketplace_entry` built
        :type entries: list
        :param engine_meta: the engine distribution's metadata, owner of
                the marketplace
        :type engine_meta: PackageMeta
        :return: path to the written manifest
        :rtype: Path
        """
