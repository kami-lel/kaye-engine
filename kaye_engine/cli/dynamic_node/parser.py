"""
parser.py

define ``register_dynamic_node_parser``
"""

import sys
from argparse import RawDescriptionHelpFormatter

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.abbr_collection import get_abbr_data
from kaye_engine.cli.dynamic_node.node_type_choices import NODE_TYPE_CHOICES
from kaye_engine.kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)
from kaye_engine.prompt.blueprint.prompt_blueprint import PromptBlueprint
from kaye_engine.prompt.dynamic_nodes import AbbrGroupNode
from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode

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

NODE_TYPE also accepts any abbr group name currently known to the
loaded abbrs.json -- consumer-defined, not listed above, eg:

    kaye-engine dynamic-node coding-terms

Abbreviation node reads its query content from stdin, optional:

    echo "use an algo to calc the avg" | kaye-engine dynamic-node abbr
"""
)


# auxiliaries  #################################################################
def _resolve_node_type(name):
    """
    resolve ``name`` against ``NODE_TYPE_CHOICES`` first, then against
    every group name known to ``get_abbr_data().groups`` -- returns
    ``(node_cls, None)`` for an engine-defined choice, ``(AbbrGroupNode,
    name)`` for a group match; raises ``ValueError`` when ``name``
    matches neither
    """
    if name in NODE_TYPE_CHOICES:
        return NODE_TYPE_CHOICES[name], None

    if name in get_abbr_data().groups.names:
        return AbbrGroupNode, name

    raise ValueError(
        "unrecognized NODE_TYPE: {}; expected one of {} or a known abbr "
        "group name".format(repr(name), list(NODE_TYPE_CHOICES))
    )


def _dynamic_node_main(args):
    set_logging_level_by_namespace(args, logger=logger)

    node_cls, group_name = _resolve_node_type(args.NODE_TYPE)

    dummy_root = PromptCorpusNode(_ROOT_NODE_NAME, None, [])
    node = (
        node_cls(dummy_root, group_name=group_name)
        if group_name is not None
        else node_cls(dummy_root)
    )

    blueprint = PromptBlueprint.create_from_node(
        node.name, corpus_tree=dummy_root
    )

    query = sys.stdin.read() if not sys.stdin.isatty() else ""

    generate_kwargs = {}
    if args.NODE_TYPE == "abbr":
        generate_kwargs["query"] = query

    prompt = blueprint.generate_prompt(**generate_kwargs)

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
        help=(
            "dynamic node type to render: an engine-defined choice "
            "({}) or a known abbr group name".format(
                ", ".join(NODE_TYPE_CHOICES)
            )
        ),
    )
    add_verbose_arguments(dynamic_node_parser)

    dynamic_node_parser.set_defaults(func=_dynamic_node_main)
