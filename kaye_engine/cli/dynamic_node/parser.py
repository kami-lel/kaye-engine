"""
parser.py

define ``register_dynamic_node_parser``
"""

import sys
from argparse import RawDescriptionHelpFormatter

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.abbr_collection import abbr_group_registry
from kaye_engine.cli.dynamic_node.node_type_choices import (
    ENGINE_DEFINED_NODES,
    list_all_node_type_names,
)
from kaye_engine.kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)
from kaye_engine.prompt.blueprint.prompt_blueprint import PromptBlueprint
from kaye_engine.prompt.dynamic_nodes import AbbrGroupNode
from kaye_engine.prompt.prompt_corpus_loader import get_default_corpus_tree
from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################
_HELP = "render a single dynamic node"

# root heading of the dummy corpus tree built for this command
_ROOT_NODE_NAME = "○"


# auxiliaries  #################################################################
def _build_description():
    return _HELP + """

renders a blueprint made of ONLY the given NODE dynamic node,
result is printed to stdout

run `kaye-engine dynamic-node ls` to list available NODE values

when NODE=abbr, reads query content from stdin, optional:

    echo "use an algo to calc the avg" | kaye-engine dynamic-node abbr
"""


def _resolve_node_type(name):
    """
    resolve ``name`` against ``ENGINE_DEFINED_NODES`` and known abbr
    group names -- returns ``(node_cls, None)`` for an engine-defined
    choice, ``(AbbrGroupNode, name)`` for a group match; raises
    ``ValueError`` when ``name`` matches neither
    """
    node_cls = ENGINE_DEFINED_NODES.get(name)
    if node_cls is not None:
        return node_cls, None

    if name in abbr_group_registry:
        return AbbrGroupNode, name

    raise ValueError("unrecognized NODE: {}".format(repr(name)))


def _dynamic_node_main(args):
    set_logging_level_by_namespace(args, logger=logger)

    if args.NODE == "ls":
        for name in list_all_node_type_names():
            print(name)
        return

    try:
        node_cls, group_name = _resolve_node_type(args.NODE)
    except ValueError as err:
        logger.error(str(err))
        raise SystemExit(1) from err

    try:
        heading = "(" + args.NODE + ")"

        try:
            default_tree = get_default_corpus_tree()
        except ValueError:
            default_tree = None

        has_authored_heading = default_tree is not None and any(
            child.name == heading for child in default_tree.children
        )

        if has_authored_heading:
            # reuse the already-loaded default corpus tree so this node's
            # authored preface (from its "(...)" section) is included
            corpus_tree = default_tree
            node_name = heading
        else:
            dummy_root = PromptCorpusNode(_ROOT_NODE_NAME, None, [])
            node = (
                node_cls(dummy_root, group_name=group_name)
                if group_name is not None
                else node_cls(dummy_root)
            )
            corpus_tree = dummy_root
            node_name = node.name

        blueprint = PromptBlueprint.create_from_node(
            node_name, corpus_tree=corpus_tree
        )

        query = sys.stdin.read() if not sys.stdin.isatty() else ""

        generate_kwargs = {}
        if args.NODE == "abbr":
            generate_kwargs["query"] = query

        prompt = blueprint.generate_prompt(**generate_kwargs)

        print(prompt)
    except (ValueError, TypeError, KeyError, NotImplementedError) as err:
        logger.critical(str(err))
        raise SystemExit(1) from err


# Public API  ##################################################################
def register_dynamic_node_parser(cli_subparser):
    """
    register the ``kaye-engine dynamic-node`` subcommand parser
    """
    dynamic_node_parser = cli_subparser.add_parser(
        "dynamic-node",
        help=_HELP,
        description=_build_description(),
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["dn"],
    )

    # add arguments  -------------------------------------------------------
    # positional
    dynamic_node_parser.add_argument(
        "NODE",
        help="dynamic node type to render; NODE=ls to list available values",
    )
    add_verbose_arguments(dynamic_node_parser)

    dynamic_node_parser.set_defaults(func=_dynamic_node_main)
