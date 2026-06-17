"""export for Claude Code as a plugin and User System Prompt file"""

from pathlib import Path

# constants  ===================================================================

_DEFAULT_CLAUDE_FOLDER = Path.home() / ".claude"


def register_cli_claude_code_parser(  ##########################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    code_parser = cli_subparser.add_parser(
        "code",
        help=__doc__,
        description=__doc__,
        aliases=["c"],
    )

    code_parser.add_argument(
        "folder",
        nargs="?",
        metavar="FOLDER",
        type=Path,
        default=_DEFAULT_CLAUDE_FOLDER,
        help="path to local .claude/ folder; default: ~/.claude",
    )

    def _code_main(args):
        folder = args.folder
        pass  # TODO

    code_parser.set_defaults(func=_code_main)
