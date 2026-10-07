"""
export_image_prompt_parser.py

define ``register_export_image_prompt_parser``
"""

import os
from argparse import RawDescriptionHelpFormatter

import kamilog
from kaye_engine.deed import track
from kaye_engine import LOGGER_NAME, PACKAGE_NAME
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.exportable import (
    get_exportable,
    image_prompt_exportable_registry,
)
from kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)
from kaye_engine.prompt.blueprint.render_mode import RenderMode
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.cli.dry_run import (
    apply_dry_run_arg,
    build_dry_run_parent_parser,
    is_dry_run,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################
# image-prompt positive field must never carry {avoid} content; that content
# is written separately, to a sibling "<name>-AVOID.md" file, holding bare
# {avoid} content with no titles (NEGATIVE | IMAGE). IMAGE also forces
# sparseness=1, superseding the explicit sparseness=0 below.
_IMAGE_PROMPT_SPARSE_RENDER_PROFILE = RenderProfile(
    sparseness=0, mode=RenderMode.IMAGE
)
_AVOID_FILE_SUFFIX = "-AVOID"

_HELP = "export the image-prompt exportable subset as Markdown files"

_DESCRIPTION = _HELP + """

writes every exportable in the image-prompt export subset to FOLDER, one
Markdown file per canonical name, plus a "<canonical_name>-AVOID.md"
sibling wherever that entry has real {avoid} content:

    kaye-engine export-image-prompt FOLDER
"""


# auxiliaries  #################################################################
def _avoid_content(exportable):
    """
    render an exportable's negative prompt -- every ``{avoid}``
    sidecar anywhere in its blueprint tree, structure-preserving -- if
    any

    :param exportable: exportable to render the negative prompt from
    :type exportable: Exportable
    :return: rendered negative prompt, or ``""`` when unavailable
    :rtype: str
    """
    if not exportable.supports_negative_content:
        return ""
    return exportable.content(
        profile=_IMAGE_PROMPT_SPARSE_RENDER_PROFILE.merge(
            # ``mode`` is a scalar field -- ``.merge()`` lets ``other``
            # win outright rather than union bits, so NEGATIVE must be
            # combined with IMAGE here explicitly to keep both
            RenderProfile(mode=RenderMode.NEGATIVE | RenderMode.IMAGE)
        )
    )


def _write_text_file(path, content):
    deed = (
        track(logger).owr_file if os.path.exists(path)
        else track(logger).create_file
    )
    with deed(path):
        if not is_dry_run():
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)


def _export_image_prompt_main(args):
    set_logging_level_by_namespace(args, logger=logger)
    apply_dry_run_arg(args)
    logger.enter("{} export-image-prompt".format(PACKAGE_NAME))
    check_corpus_setup_for_cli()

    if not os.path.isdir(args.folder):
        with track(logger).create_dir(args.folder):
            if not is_dry_run():
                os.makedirs(args.folder, exist_ok=True)

    for canonical_name in sorted(image_prompt_exportable_registry):
        exportable = get_exportable(canonical_name)

        positive_path = os.path.join(args.folder, canonical_name + ".md")
        _write_text_file(
            positive_path,
            exportable.content(profile=_IMAGE_PROMPT_SPARSE_RENDER_PROFILE),
        )

        avoid_content = _avoid_content(exportable)
        if avoid_content:
            negative_path = os.path.join(
                args.folder, canonical_name + _AVOID_FILE_SUFFIX + ".md"
            )
            _write_text_file(negative_path, avoid_content)

    logger.done("export export-image-prompt:\t" + str(args.folder))


# Public API  ##################################################################
def register_export_image_prompt_parser(cli_subparser):
    """
    register the ``kaye-engine export-image-prompt`` subcommand parser
    """
    export_image_prompt_parser = cli_subparser.add_parser(
        "export-image-prompt",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["img"],
        parents=[build_dry_run_parent_parser()],
    )

    # add arguments  -----------------------------------------------------------
    export_image_prompt_parser.add_argument(
        "folder",
        metavar="FOLDER",
        help="directory to write the Markdown files into; created if"
        " missing",
    )
    add_verbose_arguments(export_image_prompt_parser)

    export_image_prompt_parser.set_defaults(func=_export_image_prompt_main)
