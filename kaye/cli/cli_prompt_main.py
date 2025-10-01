"""dynamically generate system prompt with a prompt blueprint
as a subset of the prompt corpus"""

# todo import/export w/ OpenWebUI
# todo import/export w/ dify

from kaye.cli.cli_prompt_ls import register_cli_prompt_ls_parser


def register_cli_prompt_parser(cli_subparser):
    cli_prompt_parser = cli_subparser.add_parser(
        "prompt",
        help=__doc__,
        description=__doc__,
        aliases=["p"],
    )

    def _cli_prompt_parser_main(_):
        # when calling ``python -m kaye prompt``
        cli_prompt_parser.print_help()

    cli_prompt_parser.set_defaults(func=_cli_prompt_parser_main)

    cli_prompt_subparser = cli_prompt_parser.add_subparsers(
        description="utility functions related to prompt generation"
    )

    register_cli_prompt_ls_parser(cli_prompt_subparser)
