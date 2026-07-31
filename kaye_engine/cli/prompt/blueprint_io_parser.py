"""
blueprint_io_parser.py

define ``blueprint_io_parser``, ``load_blueprint_from_args``,
``write_blueprint_result``
"""

from argparse import FileType, ArgumentParser

from kaye_engine import logger
from kaye_engine.prompt.blueprint import blueprint_registry
from kaye_engine.prompt.blueprint.prompt_blueprint import PromptBlueprint

# defining args shared by generate_parser and show_parser
blueprint_io_parser = ArgumentParser(add_help=False)
# positional argument
blueprint_io_parser.add_argument(
    "BLUEPRINT",
    help="embedded blueprints name",
    type=str,
)
# options
blueprint_io_parser.add_argument(
    "-f",
    "--source-file",
    action="store_true",
    help="load blueprint from path BLUEPRINT",
)
blueprint_io_parser.add_argument(
    "-F",
    "--target-file",
    metavar="FILE",
    type=FileType(mode="w"),
    nargs="?",
    help="save result to FILE",
)
blueprint_io_parser.add_argument(
    "-C",
    "--no-comment",
    action="store_true",
    help="disable last-line comment in result",
)


# Public API  ###################################################################
def load_blueprint_from_args(args):
    """
    load the blueprint identified by ``args.BLUEPRINT``,
    either from the blueprint registry or from a source file
    """
    if args.source_file:
        # fixme utilize kamilog here
        with open(args.BLUEPRINT, "r", encoding="utf-8") as blueprint_file:
            blueprint = PromptBlueprint.parse(blueprint_file.read())
        return blueprint, args.BLUEPRINT

    try:
        registry = blueprint_registry[args.BLUEPRINT]
    except KeyError as err:
        logger.critical("unknown blueprint:\t{}".format(args.BLUEPRINT))
        raise SystemExit(1) from err

    return registry.blueprint, registry.display_name


def write_blueprint_result(text, target_file):
    """
    write ``text`` to ``target_file``, or print it when ``target_file``
    is ``None``
    """
    if target_file is None:
        print(text)
    else:
        # fixme utilize kamilog here
        target_file.write(text)
