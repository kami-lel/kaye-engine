"""
parser.py

define ``register_upsert_open_webui_skills_parser``
"""

import os
import sys
from argparse import RawDescriptionHelpFormatter

from kaye_engine import PACKAGE_NAME, kamilog
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.open_webui import LOGGER_OPEN_WEBUI_NAME
from kaye_engine.cli.open_webui.client import (
    DEFAULT_BASE_URL,
    OpenWebUIClient,
    OpenWebUIError,
)
from kaye_engine.cli.open_webui.sync import sync_skills

__all__ = ("register_upsert_open_webui_skills_parser",)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_OPEN_WEBUI_NAME)

# constants  ###################################################################
API_KEY_ENV_VAR = "OWU_API_KEY"

_HELP = "push every exportable into Open WebUI as a skill"

_DESCRIPTION = _HELP + """

creates new skills and updates changed ones through the Open WebUI
Skills REST API; unchanged skills are left alone:

    OWU_API_KEY=sk-... kaye-engine upsert-open-webui-skills
    kaye-engine o --dry-run
"""


# auxiliaries  #################################################################
def _resolve_api_key(args):
    return args.api_key or os.environ.get(API_KEY_ENV_VAR, "")


def _build_main(parser):

    def _upsert_open_webui_skills_main(args):
        kamilog.set_logging_level_by_namespace(args, logger=logger)
        logger.enter("{} upsert-open-webui-skills".format(PACKAGE_NAME))
        check_corpus_setup_for_cli()

        api_key = _resolve_api_key(args)
        if not api_key:
            parser.error(
                "no API key: pass --api-key or set {}".format(API_KEY_ENV_VAR)
            )
        client = OpenWebUIClient(args.base_url, api_key)

        try:
            summary = sync_skills(
                client, is_dry_run=args.dry_run, should_prune=args.prune
            )
        except OpenWebUIError as err:
            logger.fail("fetch remote skills:\t{}".format(err))
            sys.exit(1)

        logger.done(
            "created {}, updated {}, skipped {}, pruned {}, failed {}".format(
                len(summary.created),
                len(summary.updated),
                len(summary.skipped),
                len(summary.pruned),
                len(summary.failed),
            )
        )
        if summary.failed:
            sys.exit(1)

    return _upsert_open_webui_skills_main


# Public API  ##################################################################
def register_upsert_open_webui_skills_parser(cli_subparser):
    """
    register the ``kaye-engine upsert-open-webui-skills`` subcommand parser
    """
    owu_parser = cli_subparser.add_parser(
        "upsert-open-webui-skills",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["o"],
    )

    # add arguments  -----------------------------------------------------------
    owu_parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Open WebUI server root; default: {}".format(DEFAULT_BASE_URL),
    )
    owu_parser.add_argument(
        "--api-key",
        default="",
        help="API key; default: the {} environment variable".format(
            API_KEY_ENV_VAR
        ),
    )
    owu_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report what would change without writing",
    )
    owu_parser.add_argument(
        "--prune",
        action="store_true",
        help="delete remote skills absent locally",
    )
    kamilog.add_verbose_arguments(owu_parser)

    owu_parser.set_defaults(func=_build_main(owu_parser))
