"""export the kaye plugin and User System Prompt for Claude Code"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

from kaye_engine import PACKAGE_NAME, kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.plugin_marketplace_name import (
    check_setup_for_claude_cli,
)
from kaye_engine.cli.claude.plugin.export_folder import export_plugin_as_folder
from kaye_engine.cli.claude.user_prompt.parser import (
    DEFAULT_CLAUDE_FOLDER,
    find_user_system_prompt_file,
)
from kaye_engine.cli.claude.user_prompt.export import (
    export_user_system_prompt_file,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# constants  ###################################################################
_DESCRIPTION = __doc__ + """

writes CLAUDE.md as the User System Prompt (Chat + Coder blueprint) and
exports the kaye plugin into plugins/.

CLAUDE_FOLDER/  (default: ~/.claude)
├── CLAUDE.md  (User System Prompt)
└── plugins/
    └── PLUGIN_NAME/
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            ├── coder-python/
            │   └── SKILL.md
            └── ~~  (one folder per remaining skill)
"""


# pylint: disable=missing-function-docstring
def register_code_parser(cli_subparser):  ######################################
    code_parser = cli_subparser.add_parser(
        "code",
        help=__doc__,
        description=_DESCRIPTION,
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
        logger.enter("{} claude code".format(PACKAGE_NAME))
        check_setup_for_claude_cli()

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
