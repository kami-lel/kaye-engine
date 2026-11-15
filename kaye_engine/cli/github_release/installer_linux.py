"""
installer_linux.py

define ``build_linux_installer`` -- the Linux VS Code installer, one
self-extracting file: the static ``install.sh`` header copied unchanged,
then a tar.gz of ``payload/``; run as ``bash NAME.run``
"""

import io
import tarfile
import tempfile
from pathlib import Path

import kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.dry_run import is_dry_run
from kaye_engine.deed import format_size, track

from .installer_stage import (
    get_installer_template_path,
    stage_installer_payload,
)

__all__ = ("LINUX_TEMPLATE_NAME", "build_linux_installer")

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# constants  ###################################################################
LINUX_TEMPLATE_NAME = "install.sh"

_EXECUTABLE_MODE = 0o755


# Public API  ##################################################################
def build_linux_installer(dest, *, render_profile=None):
    """
    write the Linux installer to ``dest``, mode 755

    the file is the ``install.sh`` template bytes, which end at a marker
    line and an ``exit``, followed by the gzip tar of ``payload/``; the
    script is copied byte for byte and carries no consumer name


    :param dest: the file to write, named by the caller; its folder must
            exist
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

        header = get_installer_template_path(LINUX_TEMPLATE_NAME).read_bytes()
        with tempfile.TemporaryDirectory() as stage:
            payload = Path(stage) / "payload"
            stage_installer_payload(payload, render_profile=render_profile)
            archive = _pack_payload(payload)
        dest.write_bytes(header + archive)
        dest.chmod(_EXECUTABLE_MODE)
        deed.stats = format_size(dest.stat().st_size)


# Auxiliaries  #################################################################
def _normalize(info):
    """
    drop the owner so the unpack never depends on who built the archive
    """
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    return info


def _pack_payload(payload):
    """
    :return: gzip tar bytes of ``payload`` stored under ``payload/``
    :rtype: bytes
    """
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        tar.add(payload, arcname="payload", filter=_normalize)
    return buffer.getvalue()
