"""
export.py

define ``export_codex_plugins_as_folders``
"""

from kaye_engine.cli.codex.platform import CODEX_PLATFORM
from kaye_engine.cli.plugin_platform import export as platform_export


def export_codex_plugins_as_folders(
    parent_folder, *, render_profile=None, consumer_name=None
):
    """
    export every consumer holding an exportable as its own Codex plugin
    folder: ``<parent_folder>/<consumer>/`` with ``plugin.json``,
    ``.codex-plugin/plugin.json`` and ``skills/``


    :param parent_folder: destination directory to write the plugins into
    :type parent_folder: Path-like
    :param render_profile: forwarded to every skill render
    :type render_profile: RenderProfile, optional
    :param consumer_name: export only the consumer of this canonical
            name; every plugin consumer when ``None``
    :type consumer_name: str, optional
    :return: path of each created plugin directory
    :rtype: list[Path]
    :raises ValueError: when ``consumer_name`` matches no plugin consumer
    """
    return platform_export.export_plugins_as_folders(
        CODEX_PLATFORM,
        parent_folder,
        render_profile=render_profile,
        consumer_name=consumer_name,
    )
