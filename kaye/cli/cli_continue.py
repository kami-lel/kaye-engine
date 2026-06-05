"""update Continue local config folder by exporting all current Kaye prompts/blueprints"""

from pathlib import Path

from kaye.continue_export import export_all_blueprint_rules

_DEFAULT_CONTINUE_FOLDER = Path.home() / ".continue"


def register_cli_continue_parser(  #############################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    continue_parser = cli_subparser.add_parser(
        "continue", help=__doc__, description=__doc__, aliases=["c"]
    )

    continue_parser.add_argument(
        "local_config_folder",
        metavar="LOCAL_CONFIG_FOLDER",
        nargs="?",
        type=Path,
        default=_DEFAULT_CONTINUE_FOLDER,
        help="path to local config folder, default: ~/.continue",
    )

    def _continue_main(args):
        rules_folder = args.local_config_folder / "rules"
        export_all_blueprint_rules(rules_folder)

    continue_parser.set_defaults(func=_continue_main)
