"""
show_parser.py

define ``register_show_subparser``
"""

from kaye import logger
from kaye.kamilog import add_verbose_arguments, set_logging_level_by_namespace

from kaye.cli.prompt.blueprint_io_parser import blueprint_io_parser
from kaye.prompt.blueprint import BLUEPRINT_REGISTRIES
from kaye.prompt.blueprint.prompt_blueprint import PromptBlueprint

# constants  ###################################################################

_HELP = "show content of any of embedded blueprints"


_DESCRIPTION = _HELP + """

more description"""


# auxiliaries  #################################################################
def _show_main(args):
    set_logging_level_by_namespace(args, logger=logger)

    if args.source_file:
        with open(args.BLUEPRINT, "r", encoding="utf-8") as blueprint_file:
            blueprint = PromptBlueprint.parse(blueprint_file.read())
        display_name = args.BLUEPRINT
    else:
        registry = BLUEPRINT_REGISTRIES[args.BLUEPRINT]
        blueprint = registry.blueprint
        display_name = registry.display_name

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

    if args.target_file is None:
        print(preview_tree)
    else:
        args.target_file.write(preview_tree)


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
