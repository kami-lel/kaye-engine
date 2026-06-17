"""export Kaye's Chat blueprint to User System Prompt file CLAUDE.md"""

from pathlib import Path

# constants  ===================================================================

_DEFAULT_PROMPT_FILE = Path.home() / ".claude" / "CLAUDE.md"


def register_cli_claude_user_prompt_parser(  ###################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    user_prompt_parser = cli_subparser.add_parser(
        "user-system-prompt",
        help=__doc__,
        description=__doc__,
        aliases=["u"],
    )

    user_prompt_parser.add_argument(
        "prompt_file",
        nargs="?",
        metavar="PROMPT_FILE",
        type=Path,
        default=_DEFAULT_PROMPT_FILE,
        help="path to CLAUDE.md file; default: ~/.claude/CLAUDE.md",
    )

    def _user_prompt_main(args):
        prompt_file = args.prompt_file
        pass  # TODO

    user_prompt_parser.set_defaults(func=_user_prompt_main)
