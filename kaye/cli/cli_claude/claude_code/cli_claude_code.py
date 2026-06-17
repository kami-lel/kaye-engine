"""export for Claude Code as a plugin and User System Prompt file"""

from pathlib import Path

from kaye.cli.cli_claude.claude_plugin.export_plugin_as_folder import (
    export_plugin_as_folder,
)
from kaye.cli.cli_claude.user_prompt.cli_claude_user_prompt import (
    DEFAULT_CLAUDE_FOLDER,
    find_user_system_prompt_file,
)
from kaye.cli.cli_claude.user_prompt.export_user_file import (
    export_user_system_prompt_file,
)


def register_cli_claude_code_parser(  ##########################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    code_parser = cli_subparser.add_parser(
        "code",
        help=__doc__,
        description=__doc__,
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

    def _code_main(args):
        folder = args.folder
        export_plugin_as_folder(folder)
        export_user_system_prompt_file(find_user_system_prompt_file(folder))

    code_parser.set_defaults(func=_code_main)
