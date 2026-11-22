"""
export_plugin_as_folder.py

define ``export_plugin_as_folder``, ``export_plugins_as_folders``
"""

from kaye_engine.cli.claude.platform import CLAUDE_PLATFORM
from kaye_engine.cli.plugin_platform import export as platform_export

# entry point  #################################################################


def export_plugin_as_folder(
    parent_folder, consumer, *, render_profile=None, quiet=False
):
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
    :param quiet: whether to log the finished plugin at ``DEBUG`` rather
            than ``SUCC``, for a caller that reports the result itself
    :type quiet: bool
    :return: path to the created plugin directory
    :rtype: Path
    """
    return platform_export.export_plugin_as_folder(
        CLAUDE_PLATFORM,
        parent_folder,
        consumer,
        render_profile=render_profile,
        quiet=quiet,
    )


def export_plugins_as_folders(
    parent_folder, *, render_profile=None, consumer_names=None
):
    """
    export every consumer holding an exportable as its own plugin folder


    :param parent_folder: destination directory to write the plugins into
    :type parent_folder: Path-like
    :param render_profile: forwarded to :func:`export_plugin_as_folder`
    :type render_profile: RenderProfile, optional
    :param consumer_names: export only the consumers of these canonical
            names, one str or an iterable; every plugin consumer when
            ``None``
    :type consumer_names: str or Iterable[str], optional
    :return: path of each created plugin directory
    :rtype: list[Path]
    :raises ValueError: when a name matches no plugin consumer
    """
    return platform_export.export_plugins_as_folders(
        CLAUDE_PLATFORM,
        parent_folder,
        render_profile=render_profile,
        consumer_name=consumer_names,
    )
