"""TODO write docstring for cli"""

from pathlib import Path

from kaye.continue_support import update_continue_local_config_folder

_DEFAULT_CONTINUE_FOLDER = Path.home() / ".continue"


def register_cli_continue_parser(cli_subparser):
    continue_parser = cli_subparser.add_parser(
        "continue", help=__doc__, description=__doc__, aliases=["c"]
    )

    continue_parser.add_argument(
        "local_config_folder",
        metavar="local-config-folder",
        nargs="?",
        type=Path,
        default=_DEFAULT_CONTINUE_FOLDER,
        help="path to the local config folder (default: ~/.continue)",
    )

    def _continue_main(args):
        update_continue_local_config_folder(args.local_config_folder)

    continue_parser.set_defaults(func=_continue_main)
