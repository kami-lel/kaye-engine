"""
comfy_ui_export_parser.py

define ``register_comfy_ui_export_parser``
"""

import os
from argparse import RawDescriptionHelpFormatter

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.exportable import comfy_ui_exportable_registry, get_exportable
from kaye_engine.kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)
from kaye_engine.prompt.blueprint.render_profile import RenderProfile

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################
# ComfyUI's positive field must never carry {avoid} content; that content
# is written separately, to a sibling "<name>-AVOID.md" file
_COMFY_UI_SPARSE_RENDER_PROFILE = RenderProfile(sparseness=0)
_AVOID_FILE_SUFFIX = "-AVOID"

_HELP = "export the ComfyUI exportable subset as Markdown files"

_DESCRIPTION = _HELP + """

writes every exportable in the ComfyUI export subset to FOLDER, one
Markdown file per canonical name, plus a "<canonical_name>-AVOID.md"
sibling wherever that entry has real {avoid} content:

    kaye-engine comfy-ui-export FOLDER
"""


# auxiliaries  #################################################################
def _avoid_content(exportable):
    """
    read an exportable's ``{avoid}`` sidecar content, if any

    :param exportable: exportable to read the sidecar from
    :type exportable: Exportable
    :return: raw ``{avoid}`` content, or ``""`` when unavailable
    :rtype: str
    """
    sidecars = getattr(
        getattr(exportable, "blueprint", None), "sidecars", None
    )
    return getattr(sidecars, "avoid", "") or ""


def _comfy_ui_export_main(args):
    set_logging_level_by_namespace(args, logger=logger)
    check_corpus_setup_for_cli()

    os.makedirs(args.folder, exist_ok=True)

    for canonical_name in sorted(comfy_ui_exportable_registry):
        exportable = get_exportable(canonical_name)

        positive_path = os.path.join(args.folder, canonical_name + ".md")
        with open(positive_path, "w", encoding="utf-8") as positive_file:
            positive_file.write(
                exportable.content(profile=_COMFY_UI_SPARSE_RENDER_PROFILE)
            )

        avoid_content = _avoid_content(exportable)
        if avoid_content:
            negative_path = os.path.join(
                args.folder, canonical_name + _AVOID_FILE_SUFFIX + ".md"
            )
            with open(
                negative_path, "w", encoding="utf-8"
            ) as negative_file:
                negative_file.write(avoid_content)


# Public API  ##################################################################
def register_comfy_ui_export_parser(cli_subparser):
    """
    register the ``kaye-engine comfy-ui-export`` subcommand parser
    """
    comfy_ui_export_parser = cli_subparser.add_parser(
        "comfy-ui-export",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["y"],
    )

    # add arguments  -----------------------------------------------------------
    comfy_ui_export_parser.add_argument(
        "folder",
        metavar="FOLDER",
        help="directory to write the Markdown files into; created if"
        " missing",
    )
    add_verbose_arguments(comfy_ui_export_parser)

    comfy_ui_export_parser.set_defaults(func=_comfy_ui_export_main)
