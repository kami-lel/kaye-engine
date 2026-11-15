"""
installer_windows.py

define ``build_windows_installer`` -- the Windows VS Code installer zip:
``install.cmd`` and ``place-payload-into-claude-folder.ps1``
copied unchanged from the packaged templates, plus ``payload/``
"""

import shutil
import tempfile
import zipfile
from pathlib import Path

import kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.dry_run import is_dry_run
from kaye_engine.deed import format_size, track

from .installer_stage import (
    get_installer_template_path,
    stage_installer_payload,
)

__all__ = ("WINDOWS_TEMPLATE_NAMES", "build_windows_installer")

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# constants  ###################################################################
WINDOWS_TEMPLATE_NAMES = (
    "install.cmd",
    "place-payload-into-claude-folder.ps1",
)


# Public API  ##################################################################
def build_windows_installer(dest, *, render_profile=None):
    """
    write the Windows installer zip to ``dest``

    the zip root holds the two static scripts and ``payload/``; the scripts
    are copied byte for byte and carry no consumer name


    :param dest: the zip file to write, named by the caller; its folder
            must exist
    :type dest: Path-like
    :param render_profile: render options forwarded to stage 1
    :type render_profile: RenderProfile, optional
    """
    dest = Path(dest)
    with track(logger).create_zip("installer", dest) as deed:
        deed.level = kamilog.DONE
        if is_dry_run():
            deed.stats = "size n/a"
            return

        with tempfile.TemporaryDirectory() as stage:
            stage = Path(stage)
            for name in WINDOWS_TEMPLATE_NAMES:
                shutil.copyfile(get_installer_template_path(name), stage / name)
            stage_installer_payload(
                stage / "payload", render_profile=render_profile
            )
            _write_zip(stage, dest)
        deed.stats = format_size(dest.stat().st_size)


# Auxiliaries  #################################################################
def _write_zip(root, dest):
    """
    archive every file under ``root`` at the zip root, scripts first
    """
    files = sorted(
        (p for p in root.rglob("*") if p.is_file()),
        key=lambda p: (p.parent != root, p.relative_to(root).as_posix()),
    )
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(root).as_posix())
