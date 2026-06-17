"""export Kaye's Chat blueprint to User System Prompt file CLAUDE.md"""

from pathlib import Path

# helper  ######################################################################

DEFAULT_CLAUDE_FOLDER = Path.home() / ".claude"


def find_user_system_prompt_file(claude_folder):
    """
    :param claude_folder:
    :type claude_folder: Path-like
    :return: path to User System Prompt File CLAUDE.md in ``claude_folder``
    :rtype: Path-like
    """
    return claude_folder / "CLAUDE.md"


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
        default=find_user_system_prompt_file(DEFAULT_CLAUDE_FOLDER),
        help="path to CLAUDE.md file; default: ~/.claude/CLAUDE.md",
    )

    def _user_prompt_main(args):
        prompt_file = args.prompt_file
        pass  # TODO mpl claude

    user_prompt_parser.set_defaults(func=_user_prompt_main)
