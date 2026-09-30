"""
exportable_as_json_parser.py

define ``register_exportable_as_json_parser``
"""

import json
import os
from argparse import RawDescriptionHelpFormatter

import kamilog
from kaye_engine import LOGGER_NAME, PACKAGE_NAME
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.dry_run import (
    apply_dry_run_arg,
    build_dry_run_parent_parser,
    is_dry_run,
)
from kaye_engine.exportable import exportable_registry, get_exportable
from kamilog import (
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

_HELP = "export every registered exportable's content as flat JSON"

_DESCRIPTION = _HELP + """

writes every exportable currently in the registry to one flat JSON object,
keyed by canonical name and sorted by key, indented by 2 spaces:

    kaye-engine export-json                 # write ./exportable-as-json.json
    kaye-engine json -f FILE                # write to FILE instead

an existing output file is overwritten. --dry-run renders every entry and
reports the file, writing nothing.

output shape:

    {
      "coder-python": "...rendered content...",
      "style-markdown": "...rendered content..."
    }

every entry of the registry is included, each value being that entry's
content(); there is no whitelist or blacklist yet.

content is rendered with sparseness 0, which collapses every blank-line run
to nothing, while each entry's own profile still governs everything else.
{avoid} content is folded inline into each value rather than split into a
sibling entry, unlike export-image-prompt, which writes it to separate
-AVOID files.
"""


# auxiliaries  #################################################################
def _exportable_as_json_main(args):
    set_logging_level_by_namespace(args, logger=logger)
    apply_dry_run_arg(args)
    logger.enter("{} export-json".format(PACKAGE_NAME))
    check_corpus_setup_for_cli()

    canonical_names = sorted(exportable_registry)
    content_by_name = {}
    for canonical_name in canonical_names:
        content_by_name[canonical_name] = get_exportable(
            canonical_name
        ).content(profile=_SPARSE_RENDER_PROFILE)
        logger.succ("render exportable:\t" + canonical_name)

    deed = (
        logger.track.owr_file
        if os.path.exists(args.output_file)
        else logger.track.create_file
    )
    with deed(args.output_file):
        if not is_dry_run():
            with open(args.output_file, "w", encoding="utf-8") as output_file:
                json.dump(
                    content_by_name, output_file, indent=2, sort_keys=True
                )

    logger.done("export export-json:\t" + str(args.output_file))


# Public API  ##################################################################
def register_exportable_as_json_parser(cli_subparser):
    """
    register the ``kaye-engine export-json`` subcommand parser
    """
    export_json_parser = cli_subparser.add_parser(
        "export-json",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["json"],
        parents=[build_dry_run_parent_parser()],
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
    add_verbose_arguments(export_json_parser)

    export_json_parser.set_defaults(func=_exportable_as_json_main)
