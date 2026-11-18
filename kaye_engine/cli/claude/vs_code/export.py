"""
export_vs_code_extension.py

define ``export_vs_code_extension`` -- the command's entry: stage 1
(:func:`generate_vs_code_payload`) into a temp folder, then stage 2
(:func:`place_vs_code_payload`) into the Claude folder
"""

import tempfile
from pathlib import Path

import kamilog
from kaye_engine.badge import TMP_BADGE
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.dry_run import live_run
from kaye_engine.deed import tmp_deeds, tmp_roots

from .payload import generate_vs_code_payload
from .place import place_vs_code_payload

# from .settings import update_settings_json

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# entry point  #################################################################


def export_vs_code_extension(claude_folder, *, render_profile=None):
    """
    export CLAUDE.md and a marketplace folder into the given Claude folder,
    register the marketplace and enable its plugins in ``settings.json``

    stage 1 renders the payload into a temp folder, always live even under
    a dry run, so stage 2 reports its true verdict; stage 2 writes under
    ``claude_folder`` only when the run is live

    :param claude_folder: destination .claude/ folder
    :type claude_folder: Path-like
    :param render_profile: render options forwarded to stage 1
    :type render_profile: RenderProfile, optional
    :return: path to the installed marketplace.json
    :rtype: Path
    """
    with tempfile.TemporaryDirectory(prefix="kaye-vsc-payload-") as tmp:
        logger.enter("build payload in tmp  [<tmp> = {}]".format(tmp))
        with live_run():
            with tmp_deeds(tmp):
                generate_vs_code_payload(tmp, render_profile=render_profile)
            built = sum(1 for p in Path(tmp).rglob("*") if p.is_file())
            logger.info(
                "build payload ({} files)".format(built), badges=TMP_BADGE
            )

        logger.enter("publish payload into " + str(claude_folder))
        with tmp_roots(tmp):
            marketplace_path = place_vs_code_payload(tmp, claude_folder)

    # hack hack disabled permission override, reverted to system default
    # logger.debug("update settings for git command permissions")
    # settings_path = update_settings_json(claude_folder)
    # logger.succ(
    #     "update settings for git command permissions:\t" + str(settings_path)
    # )

    return marketplace_path
