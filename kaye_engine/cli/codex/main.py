"""support OpenAI Codex"""

from argparse import RawDescriptionHelpFormatter

from kaye_engine.cli.codex import CODEX_DOC_DESCRIPTION
from kaye_engine.cli.codex.marketplace.parser import (
    register_codex_marketplace_parser,
)
from kaye_engine.cli.codex.plugin.parser import register_codex_plugin_parser
from kaye_engine.cli.codex.skills.parser import register_codex_skills_parser
from kaye_engine.cli.codex.user_prompt.parser import (
    register_codex_user_prompt_parser,
)


def register_cli_codex_parser(  ################################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    codex_parser = cli_subparser.add_parser(
        "codex",
        help=__doc__,
        description=__doc__ + CODEX_DOC_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["o"],
    )

    def _codex_parser_main(_):
        codex_parser.print_help()

    codex_parser.set_defaults(func=_codex_parser_main)

    codex_subparser = codex_parser.add_subparsers(
        description="export to Codex in various ways:"
    )

    register_codex_plugin_parser(codex_subparser)
    register_codex_marketplace_parser(codex_subparser)
    register_codex_skills_parser(codex_subparser)
    register_codex_user_prompt_parser(codex_subparser)
