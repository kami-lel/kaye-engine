"""
export_plugin_as_zip.py

define ``export_plugin_as_zip``
"""

import shutil
import tempfile
from pathlib import Path

from kaye import logger


from kaye.cli.cli_claude.export_plugin_as_folder import (
    export_plugin_as_folder,
)

# entry point  #################################################################


def export_plugin_as_zip(parent_folder, *, verbose=True):
    """
    export all Kaye blueprints as an upload-ready ``.zip`` Claude plugin

    builds the plugin folder in a temporary directory, then archives its
    contents at the archive root (no wrapper folder) so Claude Desktop's
    *Plugins > Upload* dialog accepts it directly; the upload dialog rejects
    ``.plugin`` files, so the output extension is ``.zip``


    :param parent_folder: destination directory to write the ``.zip`` into
    :type parent_folder: Path-like
    :param verbose: print the exported path when ``True``
    :type verbose: bool
    """
    parent_folder = Path(parent_folder)
    parent_folder.mkdir(parents=True, exist_ok=True)

    with (
        tempfile.TemporaryDirectory() as plugin_temp,
        tempfile.TemporaryDirectory() as zip_temp,
    ):
        plugin_root = export_plugin_as_folder(Path(plugin_temp), verbose=False)

        zip_base = Path(zip_temp) / plugin_root.name
        shutil.make_archive(str(zip_base), "zip", root_dir=plugin_root)

        dest = parent_folder / (plugin_root.name + ".zip")
        shutil.move(str(zip_base.with_suffix(".zip")), str(dest))

        logger.pass_("export plugin:\t{}".format(dest))
