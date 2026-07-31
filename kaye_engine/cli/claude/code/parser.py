"""set up Claude Code CLI with the kaye plugin and User System Prompt"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

from kaye_engine import logger, kamilog

from kaye_engine.cli.claude.plugin.export_folder import export_plugin_as_folder
from kaye_engine.cli.claude.user_prompt.parser import (
    DEFAULT_CLAUDE_FOLDER,
    find_user_system_prompt_file,
)
from kaye_engine.cli.claude.user_prompt.export import (
    export_user_system_prompt_file,
)

# Bug exported folder structure contains name: kaye-engine


#  constants  ===================================================================


_DESCRIPTION = """

writes CLAUDE.md as the User System Prompt (Chat + Coder blueprint) and
exports the kaye plugin into plugins/.

CLAUDE_FOLDER/  (default: ~/.claude)
├── CLAUDE.md  (User System Prompt)
└── plugins/
    └── kaye-engine/
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            ├── coder-python/
            │   └── SKILL.md
            └── ~~  (one folder per remaining skill)
"""


# pylint: disable=missing-function-docstring
def register_code_subparser(cli_subparser):  ###################################
    code_parser = cli_subparser.add_parser(
        "code",
        help=__doc__,
        description=__doc__ + _DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["c"],
    )

    code_parser.add_argument(
        "folder",
        nargs="?",
        metavar="CLAUDE_FOLDER",
        type=Path,
        default=DEFAULT_CLAUDE_FOLDER,
        help="path to local .claude/ folder; default: ~/.claude",
    )

    kamilog.add_verbose_arguments(code_parser)

    def _code_main(args):
        kamilog.set_logging_level_by_namespace(args, logger=logger)
        # fixme retired program name reaches verbose output; use kaye-engine
        logger.enter("kaye claude code")

        folder = args.folder

        logger.debug("export plugin as folder")
        plugin_folder = folder / "plugins"
        export_plugin_as_folder(plugin_folder)

        logger.debug("export user system prompt file")
        prompt_file = find_user_system_prompt_file(folder)
        export_user_system_prompt_file(prompt_file, use_coder=True)
        logger.succ("export user system prompt file:\t" + str(prompt_file))

        logger.done("export Claude Code folder:" + "\t" + str(folder))

    code_parser.set_defaults(func=_code_main)
