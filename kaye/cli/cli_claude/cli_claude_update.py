"""create plugin structure folder from Kaye blueprints"""

from pathlib import Path

# constants  ===================================================================

_DEFAULT_CLAUDE_PLUGINS_FOLDER = Path.home() / ".claude" / "plugins"


def register_cli_claude_update_parser(  ########################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    update_parser = cli_subparser.add_parser(
        "update", help=__doc__, description=__doc__, aliases=["u"]
    )

    update_parser.add_argument(
        "folder",
        nargs="?",
        metavar="FOLDER",
        type=Path,
        default=_DEFAULT_CLAUDE_PLUGINS_FOLDER,
        help="plugin folder path, default: ~/.claude/plugins/",
    )

    def _update_main(args):
        pass  # TODO

    update_parser.set_defaults(func=_update_main)
