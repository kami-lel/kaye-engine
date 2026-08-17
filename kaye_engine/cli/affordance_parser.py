"""
affordance_parser.py

define ``register_affordance_parser``
"""

from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.prompt.affordance_registry import affordance_registry

# constants  ###################################################################
_HELP = "list names of all registered affordances"

_DESCRIPTION = _HELP + """

prints the canonical name of each registered affordance in
affordance_registry, sorted alphabetically, one per line"""


# auxiliaries  #################################################################
def _affordance_main(_):
    check_corpus_setup_for_cli()

    for name in sorted(affordance_registry):
        print(name)


# Public API  ##################################################################
def register_affordance_parser(cli_subparser):
    """
    register the ``kaye-engine affordance`` subcommand parser
    """
    affordance_parser = cli_subparser.add_parser(
        "affordance",
        help=_HELP,
        description=_DESCRIPTION,
        aliases=["a"],
    )

    affordance_parser.set_defaults(func=_affordance_main)
