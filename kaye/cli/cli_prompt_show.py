# BUG not functional


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


SHOW_HELP_TEXT = "show content of any of embedded blueprints"
show_psr = prompt_subpsr.add_parser(
    "show",
    help=SHOW_HELP_TEXT,
    description=SHOW_HELP_TEXT,
)

# positional argument
show_psr.add_argument(
    "BLUEPRINT",
    help="name of any embedded blueprints",
    type=str,
)
# options
show_psr.add_argument(
    "-f",
    "--file",
    metavar="FILE",
    type=FileType(mode="w"),
    nargs="?",
    help="save the result to file",
)
show_psr.add_argument(
    "-l",
    "--preview-line-count",
    metavar="LINE_COUNT",
    type=int,
    nargs="?",
    help="maximum line count for each entry in blueprint preview",
    default=None,
)
show_psr.add_argument(
    "-w",
    "--preview-line-width",
    metavar="LINE_WIDTH",
    type=int,
    nargs="?",
    help="maximum line width for each entry in blueprint preview",
    default=None,
)

show_psr.set_defaults(func=_prompt_show_main)
