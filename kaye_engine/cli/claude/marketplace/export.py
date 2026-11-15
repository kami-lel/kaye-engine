"""
export_marketplace.py

define ``export_marketplace``
"""

from kaye_engine.cli.claude.platform import CLAUDE_PLATFORM
from kaye_engine.cli.claude.plugin_marketplace_name import (
    get_marketplace_name,
)
from kaye_engine.cli.plugin_platform import export as platform_export


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
    return platform_export.export_marketplace(
        CLAUDE_PLATFORM,
        marketplace_folder,
        get_marketplace_name(),
        render_profile=render_profile,
    )
