"""write the Kaye Chat blueprint as the User System Prompt CLAUDE.md"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

from kaye_engine import LOGGER_NAME, kamilog

from .export import export_user_system_prompt_file

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ===================================================================

_DESCRIPTION = """

renders the Chat blueprint (or Rapid with -r) and writes it to PROMPT_FILE
as the User System Prompt; optionally appends the Coder blueprint with -c.

PROMPT_FILE  (default: ~/.claude/CLAUDE.md)
"""

# helper  ######################################################################

DEFAULT_CLAUDE_FOLDER = Path.home() / ".claude"


def _user_prompt_main(args):
    kamilog.set_logging_level_by_namespace(args, logger=logger)
    # Fixme retired program name reaches verbose output; use kaye-engine
    logger.enter("kaye claude user-system-prompt")

    prompt_file = args.prompt_file

    export_user_system_prompt_file(
        prompt_file, use_rapid=args.rapid, use_coder=args.coder
    )

    logger.done("export user system prompt" + "\t" + str(prompt_file))


def find_user_system_prompt_file(claude_folder):
    """
    :param claude_folder:
    :type claude_folder: Path-like
    :return: path to User System Prompt File CLAUDE.md in ``claude_folder``
    :rtype: Path-like
    """
    return claude_folder / "CLAUDE.md"


# pylint: disable=missing-function-docstring
def register_user_prompt_subparser(cli_subparser):  ############################
    user_prompt_parser = cli_subparser.add_parser(
        "user-system-prompt",
        help=__doc__,
        description=__doc__ + _DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["usp"],
    )

    user_prompt_parser.add_argument(
        "prompt_file",
        nargs="?",
        metavar="PROMPT_FILE",
        type=Path,
        default=find_user_system_prompt_file(DEFAULT_CLAUDE_FOLDER),
        help="path to CLAUDE.md file; default: ~/.claude/CLAUDE.md",
    )

    user_prompt_parser.add_argument(
        "-r",
        "--rapid",
        action="store_true",
        default=False,
        help="use Rapid blueprint instead of Chat",
    )

    user_prompt_parser.add_argument(
        "-c",
        "--coder",
        action="store_true",
        default=False,
        help="append Kaye Peer Coder content after the main blueprint",
    )

    kamilog.add_verbose_arguments(user_prompt_parser)

    user_prompt_parser.set_defaults(func=_user_prompt_main)
