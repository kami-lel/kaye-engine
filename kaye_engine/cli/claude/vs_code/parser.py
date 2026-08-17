"""export the plugin as a VS Code extension marketplace folder"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

from kaye_engine import PACKAGE_NAME, kamilog
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.plugin_marketplace_name import (
    check_setup_for_claude_cli,
)
from kaye_engine.cli.claude.user_prompt.parser import (
    DEFAULT_CLAUDE_FOLDER,
)
from kaye_engine.cli.render_options_parser import (
    build_render_options_parent_parser,
    resolve_render_options,
)

from .export import export_vs_code_extension

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# constants  ===================================================================

_DESCRIPTION = """

which performs:

- writes CLAUDE.md as the User System Prompt (Chat + Coder blueprint)
- updates settings.json
- exports the kaye plugin wrapped in a marketplace under
  MARKETPLACE_FOLDER_NAME/.

CLAUDE_FOLDER/  (default: ~/.claude)
├── CLAUDE.md  (User System Prompt)
├── settings.json  (updated)
└── MARKETPLACE_FOLDER_NAME/
    ├── .claude-plugin/
    │   └── marketplace.json
    └── plugins/
        └── PLUGIN_NAME/
            ├── .claude-plugin/
            │   └── plugin.json
            └── skills/
                ├── coder-python/
                │   └── SKILL.md
                └── ~~  (one folder per remaining skill)
"""


def _vs_code_main(args):
    kamilog.set_logging_level_by_namespace(args, logger=logger)
    logger.enter("{} claude vs-code-extension".format(PACKAGE_NAME))
    check_setup_for_claude_cli()

    folder = args.folder
    render_kwargs = resolve_render_options(args, default_show_comment=True)

    marketplace_path = export_vs_code_extension(
        folder, render_kwargs=render_kwargs
    )

    logger.info("marketplace.json location:\n" + str(marketplace_path))
    logger.done("export VS Code Extension folder:\t" + str(folder))


# pylint: disable=missing-function-docstring
def register_vs_code_parser(cli_subparser):  ###################################
    vs_code_parser = cli_subparser.add_parser(
        "vs-code-extension",
        help=__doc__,
        description=__doc__ + _DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["v"],
        parents=[
            build_render_options_parent_parser(
                default_surface=("vsc",),
                default_sparseness=DEFAULT_SPARSENESS,
            )
        ],
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

    vs_code_parser.set_defaults(func=_vs_code_main)
