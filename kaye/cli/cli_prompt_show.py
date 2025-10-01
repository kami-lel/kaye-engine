"""show content of any of embedded blueprints"""

from argparse import FileType

from kaye.gen_prompt.prompt_blueprint_loader import (
    load_embedded_prompt_blueprint,
)


def register_cli_prompt_show_parser(cli_prompt_subparser):
    """
    create cli parser for ``kaye prompt show``,
    and add it to ``cli_prompt_subparser``
    """
    show_parser = cli_prompt_subparser.add_parser(
        "show",
        help=__doc__,
        description=__doc__,
    )

    # add arguments  -----------------------------------------------------------
    # positional argument
    show_parser.add_argument(
        "BLUEPRINT",
        help="name of any embedded blueprints",
        type=str,
    )
    # options
    show_parser.add_argument(
        "-f",
        "--file",
        metavar="FILE",
        type=FileType(mode="w"),
        nargs="?",
        help="save the result to file",
    )
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

    # define main function  ----------------------------------------------------
    def _prompt_show_main(args):
        # when calling ``python -m kaye prompt show``
        blueprint_name = args.BLUEPRINT
        blueprint_obj = load_embedded_prompt_blueprint(blueprint_name)

        blueprint_content = blueprint_obj.generate_preview_tree(
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
