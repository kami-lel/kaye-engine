"""export for Claude Code as a plugin and User System Prompt file"""


def register_cli_claude_code_parser(  ##########################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    code_parser = cli_subparser.add_parser(
        "code",
        help=__doc__,
        description=__doc__,
        aliases=["c"],
    )

    def _code_main(_):
        pass  # TODO

    code_parser.set_defaults(func=_code_main)
