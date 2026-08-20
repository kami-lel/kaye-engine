"""
export_plugin_as_zip.py

define ``export_plugin_as_zip``
"""

import shutil
import tempfile
from pathlib import Path

from kaye_engine import kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.setup import get_claude_cli_consumer_version

from .export_folder import (
    export_plugin_as_folder,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# entry point  #################################################################


def export_plugin_as_zip(
    parent_folder, *, includes_version=True, render_profile=None
):
    """
    export all Kaye blueprints as an upload-ready ``.zip`` Claude plugin

    builds the plugin folder in a temporary directory, then archives its
    contents at the archive root (no wrapper folder) so Claude Desktop's
    *Plugins > Upload* dialog accepts it directly; the upload dialog rejects
    ``.plugin`` files, so the output extension is ``.zip``


    :param parent_folder: destination directory to write the ``.zip`` into
    :type parent_folder: Path-like
    :param includes_version: append the configured version to the ``.zip``
            filename when ``True``
    :type includes_version: bool
    :param render_profile: render options forwarded to
            :func:`export_plugin_as_folder`
    :type render_profile: RenderProfile, optional
    """
    parent_folder = Path(parent_folder)
    try:
        parent_folder.mkdir(parents=True, exist_ok=True)
    except OSError as err:
        logger.critical(
            "cannot create destination folder:\t" + str(parent_folder)
        )
        raise SystemExit(1) from err

    with (
        tempfile.TemporaryDirectory() as plugin_temp,
        tempfile.TemporaryDirectory() as zip_temp,
    ):
        logger.debug("building plugin folder in temporary directory")
        plugin_root = export_plugin_as_folder(
            Path(plugin_temp), render_profile=render_profile
        )

        logger.debug("archiving plugin to .zip package")
        zip_base = Path(zip_temp) / plugin_root.name
        shutil.make_archive(str(zip_base), "zip", root_dir=plugin_root)

        logger.debug("moving archived plugin to destination folder")
        file_name = plugin_root.name
        if includes_version:
            file_name = "{}-{}".format(
                file_name, get_claude_cli_consumer_version()
            )
        dest = parent_folder / (file_name + ".zip")
        shutil.move(str(zip_base.with_suffix(".zip")), str(dest))

        logger.succ("export plugin:\t{}".format(dest))
