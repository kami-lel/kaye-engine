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

# Public API  ###################################################################
def load_blueprint_from_args(args):
    """
    load the blueprint identified by ``args.BLUEPRINT``, either from
    the blueprint registry by name, or from stdin when ``args.BLUEPRINT``
    is ``None``


    :return: ``(blueprint, display_name, registry)`` -- ``registry`` is the
            `BlueprintRegistry` the blueprint was looked up from, or
            ``None`` when loaded from stdin (no registry entry to consult
            for defaults)
    :rtype: tuple[PromptBlueprint, str, BlueprintRegistry or None]
    """
    if args.BLUEPRINT is None:
        blueprint = PromptBlueprint.parse(sys.stdin.read())
        return blueprint, "<stdin>", None

    try:
        registry = blueprint_registry[args.BLUEPRINT]
    except KeyError as err:
        logger.critical("unknown blueprint:\t{}".format(args.BLUEPRINT))
        raise SystemExit(1) from err

    return registry.blueprint, registry.display_name, registry
