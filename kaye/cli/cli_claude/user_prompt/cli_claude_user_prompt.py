"""export Chat blueprint as Claude user system prompts"""


def register_cli_claude_user_prompt_parser(  ###################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    user_prompt_parser = cli_subparser.add_parser(
        "user-system-prompt",
        help=__doc__,
        description=__doc__,
        aliases=["u"],
    )

    def _user_prompt_main(_):
        pass  # TODO

    user_prompt_parser.set_defaults(func=_user_prompt_main)
