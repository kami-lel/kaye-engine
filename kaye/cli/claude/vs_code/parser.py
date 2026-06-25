"""export for Claude Code VS Code Extension: CLAUDE.md and kaye_marketplace"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

from kaye import logger, kamilog

from kaye.cli.claude.user_prompt.parser import (
    DEFAULT_CLAUDE_FOLDER,
)
from .export import export_vs_code_extension

# constants  ===================================================================

_DESCRIPTION = """

install kaye into a local .claude/ folder for the Claude Code VS Code
Extension: write the Chat blueprint as CLAUDE.md and export a kaye_marketplace/
folder containing the marketplace manifest and kaye plugin.

CLAUDE_FOLDER/  (default: ~/.claude)
├── CLAUDE.md
└── kaye_marketplace/
    ├── .claude-plugin/
    │   └── marketplace.json
    └── plugins/
        └── kaye/
            ├── .claude-plugin/
            │   └── plugin.json
            └── skills/
                ├── coder-python/
                │   └── SKILL.md
                └── ~~  (one folder per remaining skill)
"""


def register_parser(  ###########################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    vs_code_parser = cli_subparser.add_parser(
        "vs-code-extension",
        help=__doc__,
        description=__doc__ + _DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["v"],
    )

    vs_code_parser.add_argument(
        "folder",
        nargs="?",
        metavar="CLAUDE_FOLDER",
        type=Path,
        default=DEFAULT_CLAUDE_FOLDER,
        help="path to local .claude/ folder; default: ~/.claude",
    )

    kamilog.add_verbose_arguments(vs_code_parser)

    def _vs_code_main(args):
        kamilog.set_logging_level_by_verbosity(args, logger=logger)
        logger.enter("kaye claude vs-code-extension")

        folder = args.folder

        export_vs_code_extension(folder)

        # TODO print information of manifest placement
        logger.done("export VS Code Extension folder:\t" + str(folder))

    vs_code_parser.set_defaults(func=_vs_code_main)
