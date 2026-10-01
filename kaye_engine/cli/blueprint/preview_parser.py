"""
preview_parser.py

define ``register_preview_parser``
"""

from argparse import RawDescriptionHelpFormatter

import kamilog
from kaye_engine import LOGGER_NAME
from kaye_engine.cli.blueprint.aux_input import get_cmd_blueprint
from kaye_engine.cli.blueprint.aux_output import (
    emit_str,
    pick_preview_fx,
    run_cmd_and_exit,
)
from kaye_engine.cli.blueprint.blueprint_arg_parser import (
    build_blueprint_arg_parser,
    build_no_dependencies_arg_parser,
)
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.comment_parser import build_comment_parent_parser
from kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################

_HELP = "preview a blueprint as a tree of its entries"


_DESCRIPTION = _HELP + """

renders the blueprint as a tree of its entries, each shown as a truncated
excerpt of its content, and prints the result to stdout; dependencies are
included unless -D is given

select BLUEPRINT by canonical name in blueprint registry:

    kaye-engine blueprint preview my-blueprint

reading blueprint from stdin, a preview tree or JSON:

    kaye-engine blueprint preview < my-blueprint.json
    cat my-tree.txt | kaye-engine blueprint preview

preview tree's depth, line count, and line width can be tuned with: -t, -l, -w
"""


# auxiliaries  #################################################################
def _preview_main(args):
    set_logging_level_by_namespace(args, logger=logger)
    check_corpus_setup_for_cli()

    loaded = get_cmd_blueprint(args.BLUEPRINT)

    show_comment = True if args.show_comment is None else args.show_comment

    preview_kwargs = {
        "show_full_tree": args.show_full_tree,
        "show_comment": show_comment,
        "display_name": loaded.display_name,
    }
    if args.preview_line_count is not None:
        preview_kwargs["content_preview_lines"] = args.preview_line_count
    if args.preview_line_width is not None:
        preview_kwargs["content_preview_width"] = args.preview_line_width

    preview_fx = pick_preview_fx(args.is_no_dependencies)

    emit_str(preview_fx(loaded.blueprint, **preview_kwargs))


# Public API  ##################################################################
def register_preview_parser(cli_subparser):
    """
    register the ``kaye blueprint preview`` subcommand parser
    """
    preview_parser = cli_subparser.add_parser(
        "preview",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["p"],
        parents=[
            build_blueprint_arg_parser(),
            build_no_dependencies_arg_parser(),
            build_comment_parent_parser(),
        ],
    )

    # add arguments  -----------------------------------------------------------
    preview_parser.add_argument(
        "-l",
        "--preview-line-count",
        metavar="LINE_COUNT",
        type=int,
        nargs="?",
        help="maximum line count for each entry in blueprint preview",
        default=None,
    )
    preview_parser.add_argument(
        "-w",
        "--preview-line-width",
        metavar="LINE_WIDTH",
        type=int,
        nargs="?",
        help="maximum line width for each entry in blueprint preview",
        default=None,
    )
    preview_parser.add_argument(
        "-t",
        "--show-full-tree",
        action="store_true",
        help="display the entire preview tree",
    )

    add_verbose_arguments(preview_parser)

    preview_parser.set_defaults(
        func=lambda args: run_cmd_and_exit(_preview_main, args)
    )
