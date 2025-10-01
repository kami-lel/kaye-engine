"""dynamically generate system prompt with a prompt blueprint
as a subset of the prompt corpus"""

# todo import/export w/ OpenWebUI
# todo import/export w/ dify


def _cli_prompt_parser_main(_):
    # when calling ``python -m kaye prompt``
    cli_prompt_parser.print_help()


# BUG
cli_prompt_parser = cli_parser.add_parser(
    "prompt",
    help=__doc__,
    description=__doc__,
    alias=["p"],
)
cli_prompt_subparser = cli_prompt_parser.add_subparsers(
    description="utility functions related to prompt generation"
)

cli_prompt_parser.set_defaults(func=_cli_prompt_parser_main)
