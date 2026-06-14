"""create .plugin compressed file from Kaye blueprints"""

from pathlib import Path


def register_cli_claude_create_parser(  ########################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    create_parser = cli_subparser.add_parser(
        "create", help=__doc__, description=__doc__, aliases=["c"]
    )

    create_parser.add_argument(
        "plugin",
        nargs="?",
        metavar="PLUGIN",
        type=Path,
        default=Path.cwd(),
        help=(
            "folder path to place created kaye.plugin files, "
            "default: current directory"
        ),
    )

    def _create_main(args):
        pass  # TODO command: kaye claude create

    create_parser.set_defaults(func=_create_main)
