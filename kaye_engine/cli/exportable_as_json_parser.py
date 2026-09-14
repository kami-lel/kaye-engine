"""
exportable_as_json_parser.py

define ``register_exportable_as_json_parser``
"""

import json
from argparse import RawDescriptionHelpFormatter

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.exportable import (
    comfy_ui_exportable_registry,
    exportable_registry,
    get_exportable,
)
from kaye_engine.kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)
from kaye_engine.prompt.blueprint.render_profile import RenderProfile

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################
_DEFAULT_OUTPUT_FILE = "exportable-as-json.json"

# sparseness=0 collapses every blank-line run to nothing; the registry
# entry's own profile still governs everything else (surface,
# affordance, usage sidecars)
_SPARSE_RENDER_PROFILE = RenderProfile(
    sparseness=0, conditional_sidecars=("avoid",)
)
# ComfyUI's positive field must never carry {avoid} content; that content
# is exported separately, under a "<name>-AVOID" key
_COMFY_UI_SPARSE_RENDER_PROFILE = RenderProfile(sparseness=0)
_AVOID_KEY_SUFFIX = "-AVOID"

_HELP = "export every registered exportable's content as flat JSON"

_DESCRIPTION = _HELP + """

writes every exportable currently in the registry to a flat JSON object,
keyed by canonical name:

    kaye-engine exportable-as-json
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


def _exportable_as_json_main(args):
    set_logging_level_by_namespace(args, logger=logger)
    check_corpus_setup_for_cli()

    if args.comfy_ui:
        canonical_names = sorted(comfy_ui_exportable_registry)
        content_by_name = {}
        for canonical_name in canonical_names:
            exportable = get_exportable(canonical_name)
            content_by_name[canonical_name] = exportable.content(
                profile=_COMFY_UI_SPARSE_RENDER_PROFILE
            )
            avoid_content = _avoid_content(exportable)
            if avoid_content:
                content_by_name[
                    canonical_name + _AVOID_KEY_SUFFIX
                ] = avoid_content
    else:
        canonical_names = sorted(exportable_registry)
        content_by_name = {
            canonical_name: get_exportable(canonical_name).content(
                profile=_SPARSE_RENDER_PROFILE
            )
            for canonical_name in canonical_names
        }

    with open(args.output_file, "w", encoding="utf-8") as output_file:
        json.dump(content_by_name, output_file, indent=2, sort_keys=True)


# Public API  ##################################################################
def register_exportable_as_json_parser(cli_subparser):
    """
    register the ``kaye-engine exportable-as-json`` subcommand parser
    """
    export_json_parser = cli_subparser.add_parser(
        "exportable-as-json",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["j"],
    )

    # add arguments  -----------------------------------------------------------
    export_json_parser.add_argument(
        "--output-file",
        "-f",
        default=_DEFAULT_OUTPUT_FILE,
        help="path to write the JSON output to; default: {}".format(
            _DEFAULT_OUTPUT_FILE
        ),
    )
    export_json_parser.add_argument(
        "--comfy-ui",
        "-y",
        action="store_true",
        help="restrict export to the ComfyUI exportable subset",
    )
    add_verbose_arguments(export_json_parser)

    export_json_parser.set_defaults(func=_exportable_as_json_main)
