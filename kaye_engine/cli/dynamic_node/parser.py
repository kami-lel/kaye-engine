"""
parser.py

define ``register_dynamic_node_parser``
"""

import sys
from argparse import RawDescriptionHelpFormatter

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)
from kaye_engine.prompt.blueprint.prompt_blueprint import PromptBlueprint
from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode

from kaye_engine.cli.dynamic_node.node_type_choices import NODE_TYPE_CHOICES

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################
_HELP = "render a single dynamic node"

# root heading of the dummy corpus tree built for this command
_ROOT_NODE_NAME = "○"


_NODE_TYPE_LIST = "\n".join(
    "{:<10}{}".format(name, cls.HEADING)
    for name, cls in NODE_TYPE_CHOICES.items()
)


_DESCRIPTION = (
    _HELP
    + """

renders a blueprint made of ONLY the given NODE_TYPE dynamic node,
result is printed to stdout

NODE_TYPE choices:

"""
    + _NODE_TYPE_LIST
    + """

Abbreviation node reads its query content from stdin, optional:

    echo "use an algo to calc the avg" | kaye-engine dynamic-node abbr
"""
)


# auxiliaries  #################################################################
def _dynamic_node_main(args):
    set_logging_level_by_namespace(args, logger=logger)

    node_cls = NODE_TYPE_CHOICES[args.NODE_TYPE]

    dummy_root = PromptCorpusNode(_ROOT_NODE_NAME, None, [])
    node_cls(dummy_root)

    blueprint = PromptBlueprint.create_from_node(
        "(" + node_cls.HEADING + ")", corpus_tree=dummy_root
    )

    generate_kwargs = {}
    if args.NODE_TYPE == "abbr":
        generate_kwargs["query"] = sys.stdin.read()

    try:
        prompt = blueprint.generate_prompt(**generate_kwargs)
    except RuntimeError as e:  # BUG better handling empty abbr
        logger.warning(str(e))
        prompt = ""

    print(prompt)


# Public API  ##################################################################
def register_dynamic_node_parser(cli_subparser):
    """
    register the ``kaye-engine dynamic-node`` subcommand parser
    """
    dynamic_node_parser = cli_subparser.add_parser(
        "dynamic-node",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["dn"],
    )

    # add arguments  -------------------------------------------------------
    # positional
    dynamic_node_parser.add_argument(
        "NODE_TYPE",
        help="dynamic node type to render",
        choices=list(NODE_TYPE_CHOICES),
    )
    add_verbose_arguments(dynamic_node_parser)

    dynamic_node_parser.set_defaults(func=_dynamic_node_main)
