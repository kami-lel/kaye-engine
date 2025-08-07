"""
CLI for Python module ``kaye``
"""

from argparse import ArgumentParser, FileType

from kaye.gen_prompt.prompt_blueprint_loader import (
    PromptBlueprint,
    get_embedded_prompt_blueprints_names,
    load_embedded_prompt_blueprint,
    load_embedded_prompt_corpus,
)

# get all available blueprints at runtime
blueprint_names = sorted(get_embedded_prompt_blueprints_names())


# Main Parser: kaye ============================================================
# setup main parser
def _kaye_main(_):
    # when calling ``python -m kaye``
    kaye_psr.print_help()


kaye_psr = ArgumentParser(prog="kaye", description=__doc__)
kaye_psr.set_defaults(func=_kaye_main)
kaye_subpsr = kaye_psr.add_subparsers(title="subcommands")


# Subparser: kaye prompt =======================================================
def _prompt_main(_):
    # when calling ``python -m kaye prompt``
    prompt_psr.print_help()


PROMPT_HELP_TEXT = (
    "dynamically generate AI system prompt with a prompt blueprint"
    " as a subset of the prompt corpus"
)
prompt_psr = kaye_subpsr.add_parser(
    "prompt",
    help=PROMPT_HELP_TEXT,
    description=PROMPT_HELP_TEXT,
    aliases=["pmt", "p"],
)

prompt_psr.set_defaults(func=_prompt_main)
prompt_subpsr = prompt_psr.add_subparsers(
    description="utility functions related to prompt generation"
)


# Subparser: kaye prompt ls ----------------------------------------------------
def _prompt_ls_main(_):
    # when calling ``python -m kaye prompt ls``
    print("(all available embedded blueprints:)")
    for blueprint_name in blueprint_names:
        print(blueprint_name)


LS_HELP_TEXT = "show all available embedded blueprints"
ls_psr = prompt_subpsr.add_parser(
    "ls",
    help=LS_HELP_TEXT,
    description=LS_HELP_TEXT,
)
ls_psr.set_defaults(func=_prompt_ls_main)


# args shared by gen and show
arg_sharing_psr = ArgumentParser(add_help=False)

# positional argument
arg_sharing_psr.add_argument(
    "BLUEPRINT",
    help="name of any embedded blueprints",
    type=str,
)
# options
arg_sharing_psr.add_argument(
    "-f",
    "--file",
    metavar="FILE",
    type=FileType(mode="w"),
    nargs="?",
    help="save the result to file",
)
# options
arg_sharing_psr.add_argument(
    "-l",
    "--preview-line-count",
    metavar="LINE_COUNT",
    type=int,
    nargs="?",
    help="maximum line count for each entry in blueprint preview",
    default=None,
)
arg_sharing_psr.add_argument(
    "-w",
    "--preview-line-width",
    metavar="LINE_WIDTH",
    type=int,
    nargs="?",
    help="maximum line width for each entry in blueprint preview",
    default=None,
)


# Subparser: kaye prompt gen ---------------------------------------------------
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

    # todo interactive mode
    # todo which allow user set preview line, etc.


GEN_HELP_TEXT = "generate concrete prompt from blueprint"
gen_psr = prompt_subpsr.add_parser(
    "gen",
    help=GEN_HELP_TEXT,
    description=GEN_HELP_TEXT,
    parents=[
        arg_sharing_psr,
    ],
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


# Subparser: kaye prompt show --------------------------------------------------
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
    parents=[
        arg_sharing_psr,
    ],
)
show_psr.set_defaults(func=_prompt_show_main)


# Subparser: kaye gen_continue_config ==========================================
# TODO generate for continue extension

if __name__ == "__main__":
    parsed_args = kaye_psr.parse_args()
    parsed_args.func(parsed_args)  # call respective main function
