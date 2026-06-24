"""export Kaye's Chat blueprint to User System Prompt file CLAUDE.md"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

from kaye import logger, kamilog

from .export_user_file import export_user_system_prompt_file

# constants  ===================================================================

_DESCRIPTION = """

render Kaye's Chat blueprint and write it as the User System Prompt file,
overwriting any existing one at PROMPT_FILE.
"""

# helper  ######################################################################

DEFAULT_CLAUDE_FOLDER = Path.home() / ".claude"

# Todo option to use, eg rapid & coder


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
        description=__doc__ + _DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
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

    kamilog.add_verbose_arguments(user_prompt_parser)

    def _user_prompt_main(args):
        kamilog.set_logging_level_by_verbosity(args, logger=logger)
        logger.enter("kaye claude user-system-prompt")

        prompt_file = args.prompt_file

        export_user_system_prompt_file(prompt_file)

        logger.done("export user system prompt" + "\t" + str(prompt_file))

    user_prompt_parser.set_defaults(func=_user_prompt_main)
