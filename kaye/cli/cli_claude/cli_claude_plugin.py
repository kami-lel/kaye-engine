"""export Kaye blueprints as an Anthropic Claude plugin"""

from pathlib import Path

# constants  ===================================================================

_DEFAULT_PLUGINS_FOLDER = Path.home() / ".claude" / "plugins"


def register_cli_claude_plugin_parser(  ########################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    plugin_parser = cli_subparser.add_parser(
        "plugin",
        help=__doc__,
        description=__doc__,
        aliases=["p"],
    )

    plugin_parser.add_argument(
        "folder",
        nargs="?",
        metavar="FOLDER",
        type=Path,
        default=None,
        help="destination folder; default: ~/.claude/plugins/",
    )

    plugin_parser.add_argument(
        "-z",
        "--zip",
        action="store_true",
        dest="zip",
        help="create .plugin file; FOLDER default: current directory",
    )

    def _plugin_main(args):
        folder = args.folder
        if folder is None:
            folder = Path.cwd() if args.zip else _DEFAULT_PLUGINS_FOLDER
        pass  # TODO command: kaye claude plugin

    plugin_parser.set_defaults(func=_plugin_main)
