"""
export_plugin_as_zip.py

define ``export_plugin_as_zip``, ``export_plugins_as_zips``
"""

import logging
import shutil
import tempfile
import zipfile
from pathlib import Path

import kamilog
from kaye_engine.deed import format_size, quiet_deeds, track
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.plugin_marketplace_name import (
    get_plugin_consumers,
)
from kaye_engine.cli.dry_run import is_dry_run
from kaye_engine.skill.select import select_exportables

from .export_folder import (
    export_plugin_as_folder,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# entry point  #################################################################


def export_plugins_as_zips(
    parent_folder, *, includes_version=True, render_profile=None
):
    """
    export every consumer holding an exportable as its own ``.zip``
    plugin, each carrying its consumer's version


    :param parent_folder: destination directory to write the archives into
    :type parent_folder: Path-like
    :param includes_version: append each consumer's version to its
            ``.zip`` filename when ``True``
    :type includes_version: bool
    :param render_profile: forwarded to :func:`export_plugin_as_zip`
    :type render_profile: RenderProfile, optional
    :return: number of ``.zip`` plugins exported
    :rtype: int
    """
    consumers = get_plugin_consumers()
    for consumer in consumers:
        export_plugin_as_zip(
            parent_folder,
            consumer,
            includes_version=includes_version,
            render_profile=render_profile,
        )
    return len(consumers)


def export_plugin_as_zip(
    parent_folder, consumer, *, includes_version=True, render_profile=None
):
    """
    export one consumer's exportables as an upload-ready ``.zip`` Claude
    plugin

    builds the plugin folder in a temporary directory, then archives its
    contents at the archive root (no wrapper folder) so Claude Desktop's
    *Plugins > Upload* dialog accepts it directly; the upload dialog rejects
    ``.plugin`` files, so the output extension is ``.zip``


    :param parent_folder: destination directory to write the ``.zip`` into
    :type parent_folder: Path-like
    :param consumer: the consumer the plugin belongs to
    :type consumer: Consumer
    :param includes_version: append the consumer's version to the ``.zip``
            filename when ``True``
    :type includes_version: bool
    :param render_profile: render options forwarded to
            :func:`export_plugin_as_folder`
    :type render_profile: RenderProfile, optional
    """
    parent_folder = Path(parent_folder)
    try:
        with track(logger).create_dir(parent_folder):
            if not is_dry_run():
                parent_folder.mkdir(parents=True, exist_ok=True)
    except OSError as err:
        raise SystemExit(1) from err

    dest = parent_folder / (
        _zip_file_name(consumer, includes_version) + ".zip"
    )
    if is_dry_run():
        _report_zip_without_writing(dest, consumer)
        return

    with (
        tempfile.TemporaryDirectory() as plugin_temp,
        tempfile.TemporaryDirectory() as zip_temp,
    ):
        logger.enter("build plugin folder: " + consumer.canonical_name)
        with quiet_deeds():
            plugin_root = export_plugin_as_folder(
                Path(plugin_temp),
                consumer,
                render_profile=render_profile,
                quiet=True,
            )

        # one line for the finished archive, shown at default verbosity
        with track(logger).create_zip("plugin", dest) as deed:
            deed.level = kamilog.DONE
            logger.enter("archive plugin at zip root, no wrapper folder")
            zip_base = Path(zip_temp) / plugin_root.name
            shutil.make_archive(str(zip_base), "zip", root_dir=plugin_root)
            shutil.move(str(zip_base.with_suffix(".zip")), str(dest))
            deed.stats = "{}, {}".format(
                _count_skills(len(list((plugin_root / "skills").iterdir()))),
                format_size(dest.stat().st_size),
            )
        _log_zip_entries(dest)


# auxiliaries  #################################################################
def _zip_file_name(consumer, includes_version):
    """
    :return: archive file name of the consumer's plugin, w/o extension
    :rtype: str
    """
    if includes_version:
        return "{}-{}".format(consumer.canonical_name, consumer.version)
    return consumer.canonical_name


def _count_skills(count):
    """
    :return: skill count with its noun, eg ``1 skill``, ``23 skills``
    :rtype: str
    """
    return "{} skill{}".format(count, "" if count == 1 else "s")


def _log_zip_entries(zip_path):
    """
    log every archive entry at ``DEBUG``, read back from the written file
    """
    if not logger.isEnabledFor(logging.DEBUG):
        return
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
    for name in names:
        logger.debug("  " + name)
    logger.debug("{}: {} entries".format(zip_path.name, len(names)))


def _report_zip_without_writing(dest, consumer):
    """
    log the result line of the plugin archive, building and writing
    nothing -- the dry-run stand-in for the archive steps
    """
    skills = select_exportables(consumer=consumer.canonical_name)
    with track(logger).create_zip("plugin", dest) as deed:
        deed.level = kamilog.DONE
        deed.stats = "{}, size n/a".format(_count_skills(len(skills)))
