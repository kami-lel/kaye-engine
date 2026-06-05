"""update Continue local config folder by exporting all current Kaye prompts/blueprints"""

from pathlib import Path

from kaye.continue_export import (
    ALWAYS_APPLY_BLUEPRINT,
    CODER_BLUEPRINT_GLOBS,
    RuleFile,
)
from kaye.prompt import embedded_blueprints
from kaye.prompt.embedded_blueprints import __all__ as BLUEPRINT_NAMES

_DEFAULT_CONTINUE_FOLDER = Path.home() / ".continue"


def register_cli_continue_parser(  #############################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    continue_parser = cli_subparser.add_parser(
        "continue", help=__doc__, description=__doc__, aliases=["c"]
    )

    continue_parser.add_argument(
        "local_config_folder",
        metavar="LOCAL_CONFIG_FOLDER",
        nargs="?",
        type=Path,
        default=_DEFAULT_CONTINUE_FOLDER,
        help="path to local config folder, default: ~/.continue",
    )

    def _continue_main(args):
        folder = Path(args.local_config_folder)
        rules_folder = (folder / "rules").resolve()
        rules_folder.mkdir(parents=True, exist_ok=True)

        for name in BLUEPRINT_NAMES:
            bp = getattr(embedded_blueprints, name)
            file_path = rules_folder / "{}.md".format(name)

            print("update rule: {}".format(file_path))
            with RuleFile(file_path, encoding="utf-8") as rule:
                rule.name = bp.display_name
                rule.description = bp.description
                rule.globs = CODER_BLUEPRINT_GLOBS.get(name, [])
                rule.always_apply = name in ALWAYS_APPLY_BLUEPRINT
                rule.write_prefix()
                rule.write(bp.generate_prompt())

    continue_parser.set_defaults(func=_continue_main)
