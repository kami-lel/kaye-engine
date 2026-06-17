"""export all current Kaye Continue prompts"""

from pathlib import Path


from kaye import logger, kamilog

from .export_prompt_rules import export_prompt_rules


def register_cli_continue_prompt_parser(  ######################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    prompt_parser = cli_subparser.add_parser(
        "prompt", help=__doc__, description=__doc__, aliases=["p"]
    )

    prompt_parser.add_argument(
        "prompts_folder",
        metavar="PROMPTS_FOLDER",
        type=Path,
        help="path to prompts folder",
    )

    kamilog.add_verbose_arguments(prompt_parser)

    def _prompt_main(args):
        kamilog.set_logging_level_by_verbosity(args, logger=logger)
        logger.enter("export prompts to folder")

        folder = args.prompts_folder
        kamilog.set_logging_level_by_verbosity(args, logger=logger)

        export_prompt_rules(folder)
        logger.done("export prompts to folder:\t" + str(folder))

    prompt_parser.set_defaults(func=_prompt_main)
