"""
installer_stage.py

define ``get_installer_template_path``, ``stage_installer_payload`` --
the staging both release installers share: the static script templates and
the stage 1 payload of the VS Code extension export
"""

from pathlib import Path

import kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.vs_code.payload import generate_vs_code_payload
from kaye_engine.cli.dry_run import live_run
from kaye_engine.deed import quiet_deeds

__all__ = ("get_installer_template_path", "stage_installer_payload")

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# constants  ###################################################################
_TEMPLATE_FOLDER = Path(__file__).parent / "installer_templates"


# Public API  ##################################################################
def get_installer_template_path(name):
    """
    :param name: file name of a static installer script, e.g.
            ``install.ps1``
    :type name: str
    :return: path of that template inside the package
    :rtype: Path
    """
    return _TEMPLATE_FOLDER / name


def stage_installer_payload(payload_folder, *, render_profile=None):
    """
    write the stage 1 payload (``CLAUDE.md`` and the marketplace folder,
    one plugin per consumer of the process) into ``payload_folder``;
    always live, so a dry run may still read the result


    :param payload_folder: folder to fill, the installers' ``payload/``
    :type payload_folder: Path-like
    :param render_profile: render options forwarded to stage 1
    :type render_profile: RenderProfile, optional
    """
    with live_run(), quiet_deeds():
        generate_vs_code_payload(payload_folder, render_profile=render_profile)
