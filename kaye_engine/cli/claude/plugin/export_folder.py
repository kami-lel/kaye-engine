"""
export_plugin_as_folder.py

define ``export_plugin_as_folder``, ``export_plugins_as_folders``
"""

import kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.package_meta import read_package_meta
from kaye_engine.cli.claude.plugin_marketplace_name import (
    get_plugin_consumers,
)
from kaye_engine.skill.export_folders import (
    export_skills_as_folders,
)

from .manifest import ManifestPluginJson

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# constants  ===================================================================

_SKILLS_DIR = "skills"

# entry point  #################################################################


def export_plugin_as_folder(parent_folder, consumer, *, render_profile=None):
    """
    export one consumer's exportables as an Anthropic Claude plugin folder

    writes a ``<parent_folder>/<consumer name>/`` plugin directory
    containing a ``.claude-plugin/plugin.json`` manifest, built from the
    consumer's record and its own distribution metadata, and a ``skills/``
    directory with one skill folder per exportable of that consumer


    :param parent_folder: destination directory to write the plugin into
    :type parent_folder: Path-like
    :param consumer: the consumer the plugin belongs to
    :type consumer: Consumer
    :param render_profile: render profile forwarded to
            :func:`export_skills_as_folders`
    :type render_profile: RenderProfile, optional
    :return: path to the created plugin directory
    :rtype: Path
    """
    plugin_name = consumer.canonical_name
    plugin_root = parent_folder / plugin_name
    meta = read_package_meta(plugin_name)

    with ManifestPluginJson(plugin_root) as manifest:
        manifest.name = plugin_name
        manifest.display_name = consumer.display_name
        manifest.version = consumer.version
        manifest.description = meta.summary
        manifest.author_name = meta.author_name
        manifest.author_email = meta.author_email
        manifest.homepage = meta.homepage
        manifest.repository = meta.repository
        manifest.keywords = [
            "prompt-engineering",
            "persona",
            "agent",
            plugin_name,
        ]

    logger.debug("exporting exportables as plugin skills: " + plugin_name)
    export_skills_as_folders(
        plugin_root / _SKILLS_DIR,
        version=consumer.version,
        render_profile=render_profile,
        consumer=plugin_name,
    )

    logger.succ("export plugin:\t" + str(plugin_root))

    return plugin_root


def export_plugins_as_folders(parent_folder, *, render_profile=None):
    """
    export every consumer holding an exportable as its own plugin folder


    :param parent_folder: destination directory to write the plugins into
    :type parent_folder: Path-like
    :param render_profile: forwarded to :func:`export_plugin_as_folder`
    :type render_profile: RenderProfile, optional
    :return: path of each created plugin directory
    :rtype: list[Path]
    """
    return [
        export_plugin_as_folder(
            parent_folder, consumer, render_profile=render_profile
        )
        for consumer in get_plugin_consumers()
    ]
