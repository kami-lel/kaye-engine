"""show content of any of embedded blueprints"""

from kaye import PROGRAM_NAME, kamilog
from kaye.gen_prompt.prompt_blueprint_loader import (
    load_embedded_prompt_blueprint,
)

from .cli_prompt_generate import (
    base_gen_show_parser,
    create_blueprint_from_generate_show,
)


def register_cli_prompt_show_parser(cli_prompt_subparser):
    """
    create cli parser for ``kaye prompt show``,
    and add it to ``cli_prompt_subparser``
    """
    logger = kamilog.getLogger(PROGRAM_NAME)

    show_parser = cli_prompt_subparser.add_parser(
        "show",
        help=__doc__,
        description=__doc__,
        parents=[base_gen_show_parser],
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
    base_gen_show_parser.add_argument(
        "-t",
        "--full-preview-tree",
        action="store_true",
        help="display the entire preview tree",
    )

    kamilog.add_verbose_arguments(show_parser)

    # define main function  ----------------------------------------------------
    def _prompt_show_main(args):
        kamilog.set_logging_level_by_verbosity(args, PROGRAM_NAME)

        blueprint = create_blueprint_from_generate_show(args)

        # FIXME need tests

        blueprint_content = blueprint.generate_preview_tree(
            preview_line_count=args.preview_line_count,
            preview_line_width=args.preview_line_width,
        )

        # with --file file
        if args.file:
            with args.file as f:
                f.write(blueprint_content)
        else:
            print(blueprint_content)

    show_parser.set_defaults(func=_prompt_show_main)
