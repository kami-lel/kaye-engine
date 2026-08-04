"""
blueprint_io_parser.py

define ``blueprint_io_parser``, ``load_blueprint_from_args``,
``write_blueprint_result``
"""

import sys
from argparse import ArgumentParser

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.prompt.blueprint import blueprint_registry
from kaye_engine.prompt.blueprint.prompt_blueprint import PromptBlueprint

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# defining args shared by generate_parser and show_parser
blueprint_io_parser = ArgumentParser(add_help=False)
# positional argument
blueprint_io_parser.add_argument(
    "BLUEPRINT",
    help="embedded blueprint name",
    type=str,
    nargs="?",
    default=None,
)
# options
blueprint_io_parser.add_argument(
    "-C",
    "--no-comment",
    action="store_true",
    help="disable last-line comment in result",
)


# Public API  ###################################################################
def load_blueprint_from_args(args):
    """
    load the blueprint identified by ``args.BLUEPRINT``, either from
    the blueprint registry by name, or from stdin when ``args.BLUEPRINT``
    is ``None``
    """
    if args.BLUEPRINT is None:
        blueprint = PromptBlueprint.parse(sys.stdin.read())
        return blueprint, "<stdin>"

    try:
        registry = blueprint_registry[args.BLUEPRINT]
    except KeyError as err:
        logger.critical("unknown blueprint:\t{}".format(args.BLUEPRINT))
        raise SystemExit(1) from err

    return registry.blueprint, registry.display_name


def write_blueprint_result(text):
    """
    print ``text`` to stdout
    """
    print(text)
