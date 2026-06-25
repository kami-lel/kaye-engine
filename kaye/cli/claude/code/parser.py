"""export for Claude Code as a plugin and User System Prompt file"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

from kaye import logger, kamilog

from kaye.cli.claude.plugin.export_folder import export_plugin_as_folder
from kaye.cli.claude.user_prompt.parser import (
    DEFAULT_CLAUDE_FOLDER,
    find_user_system_prompt_file,
)
from kaye.cli.claude.user_prompt.export import export_user_system_prompt_file

#  constants  ===================================================================


_DESCRIPTION = """

install kaye into a local .claude/ folder: write the kaye plugin under
plugins/ and the Chat blueprint as the User System Prompt CLAUDE.md.

FOLDER/  (default: ~/.claude)
├── CLAUDE.md  (User System Prompt)
└── plugins/
    └── kaye/
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            ├── coder-python/
            │   └── SKILL.md
            └── ~~  (one folder per remaining skill)
"""


def register_code_subparser(cli_subparser):  ###########################################################################
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
        metavar="FOLDER",
        type=Path,
        default=DEFAULT_CLAUDE_FOLDER,
        help="path to local .claude/ folder; default: ~/.claude",
    )

    kamilog.add_verbose_arguments(code_parser)

    def _code_main(args):
        kamilog.set_logging_level_by_verbosity(args, logger=logger)
        logger.enter("kaye claude code")

        folder = args.folder

        logger.debug("export plugin as folder")
        plugin_folder = folder / "plugins"
        export_plugin_as_folder(plugin_folder)

        logger.debug("export user system prompt file")
        prompt_file = find_user_system_prompt_file(folder)
        export_user_system_prompt_file(prompt_file, use_coder=True)
        logger.succ("export user system prompt file:\t" + str(prompt_file))

        # todo CLI claude code update setting for pre compact hooks

        logger.done("export Claude Code folder:" + "\t" + str(folder))

    code_parser.set_defaults(func=_code_main)
