"""
export_plugin_as_zip.py

define ``export_plugin_as_zip``
"""

import shutil
import tempfile
from importlib.metadata import version
from pathlib import Path

from kaye import logger

from kaye import PROGRAM_NAME
from .export_folder import (
    export_plugin_as_folder,
)

# entry point  #################################################################


def export_plugin_as_zip(parent_folder, *, includes_version=True):
    """
    export all Kaye blueprints as an upload-ready ``.zip`` Claude plugin

    builds the plugin folder in a temporary directory, then archives its
    contents at the archive root (no wrapper folder) so Claude Desktop's
    *Plugins > Upload* dialog accepts it directly; the upload dialog rejects
    ``.plugin`` files, so the output extension is ``.zip``


    :param parent_folder: destination directory to write the ``.zip`` into
    :type parent_folder: Path-like
    :param includes_version: append the current package version to the
            ``.zip`` filename when ``True``
    :type includes_version: bool
    """
    parent_folder = Path(parent_folder)
    parent_folder.mkdir(parents=True, exist_ok=True)

    with (
        tempfile.TemporaryDirectory() as plugin_temp,
        tempfile.TemporaryDirectory() as zip_temp,
    ):
        logger.debug("building plugin folder in temporary directory")
        plugin_root = export_plugin_as_folder(Path(plugin_temp))

        logger.debug("archiving plugin to .zip package")
        zip_base = Path(zip_temp) / plugin_root.name
        shutil.make_archive(str(zip_base), "zip", root_dir=plugin_root)

        logger.debug("moving archived plugin to destination folder")
        file_name = plugin_root.name
        if includes_version:
            file_name = "{}-{}".format(file_name, version(PROGRAM_NAME))
        dest = parent_folder / (file_name + ".zip")
        shutil.move(str(zip_base.with_suffix(".zip")), str(dest))

        logger.succ("export plugin:\t{}".format(dest))
