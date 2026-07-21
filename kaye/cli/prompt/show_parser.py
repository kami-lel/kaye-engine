"""
show_parser.py

define ``register_show_subparser``
"""

from kaye import logger
from kaye.kamilog import add_verbose_arguments, set_logging_level_by_namespace

from kaye.cli.prompt.blueprint_io_parser import (
    blueprint_io_parser,
    load_blueprint_from_args,
    write_blueprint_result,
)

# constants  ###################################################################

_HELP = "show content of any of registered blueprints"


_DESCRIPTION = _HELP + """

renders BLUEPRINT into a preview tree via generate_blueprint(), loading
it from the registry by name or, with -f, parsing it from a source
file; the preview's depth, line count, and line width can be tuned with
-t, -l, and -w, and the result is printed to stdout or, with -F,
written to a file"""


# auxiliaries  #################################################################
def _show_main(args):
    set_logging_level_by_namespace(args, logger=logger)

    blueprint, display_name = load_blueprint_from_args(args)

    render_kwargs = {
        "show_full_tree": args.show_full_tree,
        "show_comment": not args.no_comment,
        "display_name": display_name,
    }
    if args.preview_line_count is not None:
        render_kwargs["content_preview_lines"] = args.preview_line_count
    if args.preview_line_width is not None:
        render_kwargs["content_preview_width"] = args.preview_line_width

    preview_tree = blueprint.generate_blueprint(**render_kwargs)

    write_blueprint_result(preview_tree, args.target_file)


# Public API  ##################################################################
def register_show_subparser(cli_subparser):
    """
    register the ``kaye prompt show`` subcommand parser
    """
    show_parser = cli_subparser.add_parser(
        "show",
        help=_HELP,
        description=_DESCRIPTION,
        parents=[blueprint_io_parser],
    )

    # add arguments  -----------------------------------------------------------
    # options
    show_parser.add_argument(
        "-l",
        "--preview-line-count",
        metavar="LINE_COUNT",
        type=int,
        nargs="?",
        help="maximum line count for each entry in blueprint preview",
        default=None,
    )
    show_parser.add_argument(
        "-w",
        "--preview-line-width",
        metavar="LINE_WIDTH",
        type=int,
        nargs="?",
        help="maximum line width for each entry in blueprint preview",
        default=None,
    )
    show_parser.add_argument(
        "-t",
        "--show-full-tree",
        action="store_true",
        help="display the entire preview tree",
    )

    add_verbose_arguments(show_parser)

    show_parser.set_defaults(func=_show_main)
