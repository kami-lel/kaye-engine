# BUG not functional


def _prompt_gen_main(args):
    # when calling ``python -m kaye prompt gen``

    blueprint_arg = args.BLUEPRINT

    if args.source_file:
        try:
            with open(blueprint_arg, "r", encoding="utf-8") as file:
                file_content = file.read()

        except (FileNotFoundError, OSError) as e:
            raise ValueError(
                'bad filename "{}" of BLUEPRINT with --source-file'.format(
                    blueprint_arg
                )
            ) from e

        blueprint_obj = PromptBlueprint(
            load_embedded_prompt_corpus(), file_content
        )

    else:
        blueprint_obj = load_embedded_prompt_blueprint(blueprint_arg)

    prompt_content = blueprint_obj.generate_prompt(
        hide_comment=args.no_comment
    )

    # with --file FILE
    if args.file:
        with args.file as f:
            f.write(prompt_content)
    else:
        print(prompt_content)

    # todo interactive mode which allow user set preview line, etc.


GEN_HELP_TEXT = "generate concrete prompt from blueprint"
gen_psr = prompt_subpsr.add_parser(
    "gen",
    help=GEN_HELP_TEXT,
    description=GEN_HELP_TEXT,
)


# positional argument
gen_psr.add_argument(
    "BLUEPRINT",
    help="name of any embedded blueprints",
    type=str,
)
# options
gen_psr.add_argument(
    "-f",
    "--file",
    metavar="FILE",
    type=FileType(mode="w"),
    nargs="?",
    help="save the result to file",
)
# options
gen_psr.add_argument(
    "-l",
    "--preview-line-count",
    metavar="LINE_COUNT",
    type=int,
    nargs="?",
    help="maximum line count for each entry in blueprint preview",
    default=None,
)
gen_psr.add_argument(
    "-w",
    "--preview-line-width",
    metavar="LINE_WIDTH",
    type=int,
    nargs="?",
    help="maximum line width for each entry in blueprint preview",
    default=None,
)

gen_psr.add_argument(
    "-F",
    "--source-file",
    action="store_true",
    help="provide blueprint as source file of prompt blueprint",
)
gen_psr.add_argument(
    "-C",
    "--no-comment",
    action="store_true",
    help="disable last-line prompt comment in result",
)
gen_psr.set_defaults(func=_prompt_gen_main)
