"""
export.py

define ``export_plugin_as_folder``, ``export_plugins_as_folders``,
``export_marketplace`` -- the Template Methods every plugin platform
shares; each step that differs per platform calls a ``PluginPlatform`` hook
"""

from pathlib import Path

import kamilog
from kaye_engine import PACKAGE_NAME
from kaye_engine.badge import TMP_BADGE
from kaye_engine.deed import mask_tmp_roots
from kaye_engine.skill.export_folders import export_skills_as_folders

from .consumers import get_plugin_consumers, select_plugin_consumers
from .package_meta import read_package_meta

__all__ = (
    "PLUGINS_DIR",
    "export_marketplace",
    "export_plugin_as_folder",
    "export_plugins_as_folders",
)

# constants  ###################################################################

# subfolder of a marketplace root holding its plugins
PLUGINS_DIR = "plugins"

_SKILLS_DIR = "skills"


# Public API  ##################################################################


def export_plugin_as_folder(
    platform, parent_folder, consumer, *, render_profile=None, quiet=False
):
    """
    export one consumer's exportables as a plugin folder of ``platform``

    writes ``<parent_folder>/<consumer name>/`` holding the platform's
    manifest(s), built from the consumer's record and its own distribution
    metadata, and a ``skills/`` directory with one skill folder per
    exportable of that consumer


    :param platform: the plugin platform to write for
    :type platform: PluginPlatform
    :param parent_folder: destination directory to write the plugin into
    :type parent_folder: Path-like
    :param consumer: the consumer the plugin belongs to
    :type consumer: Consumer
    :param render_profile: render profile forwarded to
            :func:`export_skills_as_folders`
    :type render_profile: RenderProfile, optional
    :param quiet: whether to log the finished plugin at ``DEBUG`` rather
            than ``SUCC``, for a caller that reports the result itself
    :type quiet: bool
    :return: path to the created plugin directory
    :rtype: Path
    """
    logger = kamilog.getLogger(platform.logger_name)
    plugin_name = consumer.canonical_name
    plugin_root = Path(parent_folder) / plugin_name
    meta = read_package_meta(plugin_name)

    platform.write_plugin_manifest(plugin_root, consumer, meta)

    logger.debug("exporting exportables as plugin skills: " + plugin_name)
    export_skills_as_folders(
        plugin_root / _SKILLS_DIR,
        version=consumer.version,
        render_profile=render_profile,
        consumer=plugin_name,
    )

    if quiet:
        logger.debug(
            mask_tmp_roots("build plugin folder:\t" + str(plugin_root)),
            badges=TMP_BADGE,
        )
    else:
        logger.succ("export plugin:\t" + str(plugin_root))

    return plugin_root


def export_plugins_as_folders(
    platform, parent_folder, *, render_profile=None, consumer_name=None
):
    """
    export every consumer holding an exportable as its own plugin folder


    :param platform: the plugin platform to write for
    :type platform: PluginPlatform
    :param parent_folder: destination directory to write the plugins into
    :type parent_folder: Path-like
    :param render_profile: forwarded to :func:`export_plugin_as_folder`
    :type render_profile: RenderProfile, optional
    :param consumer_name: export only the consumer of this canonical
            name; every plugin consumer when ``None``
    :type consumer_name: str, optional
    :return: path of each created plugin directory
    :rtype: list[Path]
    :raises ValueError: when ``consumer_name`` matches no plugin consumer
    """
    return [
        export_plugin_as_folder(
            platform, parent_folder, consumer, render_profile=render_profile
        )
        for consumer in select_plugin_consumers(consumer_name)
    ]


def export_marketplace(
    platform,
    marketplace_folder,
    name,
    *,
    plugins_dir=PLUGINS_DIR,
    render_profile=None,
    owner_distribution=PACKAGE_NAME,
):
    """
    export every consumer's plugin and write the marketplace manifest
    listing them

    writes each plugin into ``<marketplace_folder>/<plugins_dir>/<consumer>/``
    then the platform's marketplace manifest at ``marketplace_folder``,
    listing one plugin per consumer with source
    ``"./<plugins_dir>/<consumer>"``; the whole marketplace is written from
    this process's consumers, so the last export wins


    :param platform: the plugin platform to write for
    :type platform: PluginPlatform
    :param marketplace_folder: marketplace root directory
    :type marketplace_folder: Path-like
    :param name: marketplace name
    :type name: str
    :param plugins_dir: plugins folder, relative to the marketplace root,
            ``/``-separated
    :type plugins_dir: str
    :param render_profile: forwarded to :func:`export_plugin_as_folder`
    :type render_profile: RenderProfile, optional
    :param owner_distribution: installed distribution whose metadata
            describes and owns the marketplace; default: the engine
    :type owner_distribution: str
    :return: path to the written marketplace manifest
    :rtype: Path
    """
    logger = kamilog.getLogger(platform.logger_name)
    marketplace_folder = Path(marketplace_folder)

    entries = []
    for consumer in get_plugin_consumers():
        plugin_name = consumer.canonical_name
        logger.debug("exporting plugin into marketplace: " + plugin_name)
        export_plugin_as_folder(
            platform,
            marketplace_folder / plugins_dir,
            consumer,
            render_profile=render_profile,
        )
        entries.append(
            platform.build_marketplace_entry(
                consumer,
                read_package_meta(plugin_name),
                "./{}/{}".format(plugins_dir, plugin_name),
            )
        )

    return platform.write_marketplace_manifest(
        marketplace_folder,
        name,
        entries,
        read_package_meta(owner_distribution),
    )
