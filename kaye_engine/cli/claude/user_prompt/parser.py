"""render the Kaye Chat blueprint as the User System Prompt"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

from kaye_engine import kamilog
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.render_options_parser import (
    build_render_options_parent_parser,
    resolve_render_options,
)

from .export import generate_user_system_prompt

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# constants  ===================================================================

_DESCRIPTION = """

renders the Chat blueprint as the User System Prompt; the result is
printed to stdout. Optionally appends the Coder blueprint with -c.

    kaye-engine claude usp > ~/.claude/CLAUDE.md
"""

# helper  ######################################################################

DEFAULT_CLAUDE_FOLDER = Path.home() / ".claude"


def _user_prompt_main(args):
    kamilog.set_logging_level_by_namespace(args, logger=logger)
    check_corpus_setup_for_cli()

    render_kwargs = resolve_render_options(args, default_show_comment=True)

    prompt = generate_user_system_prompt(
        use_coder=args.coder,
        render_kwargs=render_kwargs,
    )

    print(prompt)


def find_user_system_prompt_file(claude_folder):
    """
    :param claude_folder:
    :type claude_folder: Path-like
    :return: path to User System Prompt File CLAUDE.md in ``claude_folder``
    :rtype: Path-like
    """
    return claude_folder / "CLAUDE.md"


# pylint: disable=missing-function-docstring
def register_user_prompt_parser(cli_subparser):  ###############################
    user_prompt_parser = cli_subparser.add_parser(
        "user-system-prompt",
        help=__doc__,
        description=__doc__ + _DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["usp"],
        parents=[
            build_render_options_parent_parser(
                default_surface=("chat", "cowork"),
                default_sparseness=DEFAULT_SPARSENESS,
                comment_short_flags=False,
            )
        ],
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
