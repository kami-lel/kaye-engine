"""export all current Kaye Continue prompts"""

from pathlib import Path

from kaye.continue_export import export_prompts

# Todo prepare for feature finish


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

    def _prompt_main(args):
        export_prompts(args.prompts_folder)

    prompt_parser.set_defaults(func=_prompt_main)
