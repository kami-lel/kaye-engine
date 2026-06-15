"""update Continue local config folder by exporting all current Kaye prompts/blueprints"""

from pathlib import Path

from kaye import logger, kamilog

from .export_abbr_rules import export_abbr_rules
from .export_blueprint_rules import export_blueprint_rules

_DEFAULT_CONTINUE_FOLDER = Path.home() / ".continue"


def register_cli_continue_config_parser(  ######################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    config_parser = cli_subparser.add_parser(
        "config", help=__doc__, description=__doc__, aliases=["c"]
    )

    config_parser.add_argument(
        "local_config_folder",
        metavar="LOCAL_CONFIG_FOLDER",
        nargs="?",
        type=Path,
        default=_DEFAULT_CONTINUE_FOLDER,
        help="path to local config folder, default: ~/.continue",
    )

    kamilog.add_verbose_arguments(config_parser)

    def _config_main(args):
        logger.enter("update Continue local config folder")
        kamilog.set_logging_level_by_verbosity(args, logger=logger)

        folder = args.local_config_folder
        rules_folder = folder / "rules"
        export_blueprint_rules(rules_folder)
        export_abbr_rules(rules_folder)
        logger.done("update Continue local config folder:\t" + str(folder))

    config_parser.set_defaults(func=_config_main)
