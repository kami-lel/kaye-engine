"""set up Claude Code VS Code Extension with the kaye marketplace and User System Prompt"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

from kaye import logger, kamilog

from kaye.cli.claude.user_prompt.parser import (
    DEFAULT_CLAUDE_FOLDER,
)
from .export import export_vs_code_extension

# constants  ===================================================================

_DESCRIPTION = """

writes CLAUDE.md as the User System Prompt (Chat + Coder blueprint) and
exports the kaye plugin wrapped in a marketplace under kaye_marketplace/.

CLAUDE_FOLDER/  (default: ~/.claude)
├── CLAUDE.md  (User System Prompt)
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


# pylint: disable=missing-function-docstring
def register_vs_code_subparser(cli_subparser):  ################################
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

        marketplace_path = export_vs_code_extension(folder)

        # FIXME better showing file
        logger.info("marketplace.json location:\n" + str(marketplace_path))
        logger.done("export VS Code Extension folder:\t" + str(folder))

    vs_code_parser.set_defaults(func=_vs_code_main)
