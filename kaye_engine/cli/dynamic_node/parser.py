"""
parser.py

define ``register_dynamic_node_parser``
"""

import sys
from argparse import RawDescriptionHelpFormatter

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.abbr_collection import abbr_glossary_registry
from kaye_engine.cli.dynamic_node.node_type_choices import (
    ENGINE_DEFINED_NODES,
    list_all_node_type_names,
)
from kaye_engine.kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)
from kaye_engine.prompt.blueprint.prompt_blueprint import PromptBlueprint
from kaye_engine.prompt.dynamic_nodes import GlossaryNode
from kaye_engine.prompt.prompt_corpus_loader import get_default_corpus_tree
from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################
_HELP = "render 1 or more dynamic nodes"

# root heading of the dummy corpus tree built for this command
_ROOT_NODE_NAME = "○"


# auxiliaries  #################################################################
def _build_description():
    return _HELP + """

renders a blueprint made of each given NODE dynamic nodes,
result for every NODE is printed to stdout under its own header

when NODE=abbr, reads query content from stdin, optional:

    echo "use an algo to calc the avg" | kaye-engine dynamic-node abbr

run to list available NODE values:

    kaye-engine dynamic-node ls
"""


def _resolve_node_type(name):
    """
    resolve ``name`` against ``ENGINE_DEFINED_NODES`` and known abbr
    glossary names -- returns ``(node_cls, None)`` for an engine-defined
    choice, ``(GlossaryNode, name)`` for a glossary match; raises
    ``ValueError`` when ``name`` matches neither
    """
    node_cls = ENGINE_DEFINED_NODES.get(name)
    if node_cls is not None:
        return node_cls, None

    if name in abbr_glossary_registry:
        return GlossaryNode, name

    raise ValueError("unrecognized NODE: {}".format(repr(name)))


def _corpus_tree_and_node_name(node_name_arg, node_cls, glossary_name):
    """
    :return: ``(corpus_tree, node_name)`` -- the default corpus tree and its
            authored "(...)" heading when ``node_name_arg`` has one, else a
            fresh dummy root and the node's own name
    :rtype: tuple[PromptCorpusNode, str]
    """
    heading = "(" + node_name_arg + ")"

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
        return default_tree, heading

    dummy_root = PromptCorpusNode(_ROOT_NODE_NAME, None, [])
    node = (
        node_cls(dummy_root, glossary_name=glossary_name)
        if glossary_name is not None
        else node_cls(dummy_root)
    )
    return dummy_root, node.name


def _render_one_node(node_name_arg, query, priority_threshold):
    """
    resolve, build, and render the blueprint for a single ``NODE`` value

    :return: the rendered prompt text for ``node_name_arg``
    :rtype: str
    """
    node_cls, glossary_name = _resolve_node_type(node_name_arg)

    corpus_tree, node_name = _corpus_tree_and_node_name(
        node_name_arg, node_cls, glossary_name
    )

    blueprint = PromptBlueprint.create_from_node(
        node_name, corpus_tree=corpus_tree
    )

    generate_kwargs = {}
    if node_name_arg == "abbr":
        generate_kwargs["query"] = query
    if glossary_name is not None and priority_threshold is not None:
        generate_kwargs["glossary_priority_threshold"] = priority_threshold

    return blueprint.generate_prompt(**generate_kwargs)


def _dynamic_node_main(args):
    set_logging_level_by_namespace(args, logger=logger)

    if args.NODE == ["ls"]:
        for name in list_all_node_type_names():
            print(name)
        return

    query = sys.stdin.read() if not sys.stdin.isatty() else ""

    for node_name_arg in args.NODE:
        try:
            prompt = _render_one_node(
                node_name_arg, query, args.priority_threshold
            )
        except ValueError as err:
            logger.error(str(err))
            raise SystemExit(1) from err
        except (TypeError, KeyError, NotImplementedError) as err:
            logger.critical(str(err))
            raise SystemExit(1) from err

        print("=== {} ===".format(node_name_arg))
        print(prompt)


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
        nargs="+",
        help="dynamic nodes to render; NODE=ls: list available node values",
    )
    dynamic_node_parser.add_argument(
        "-t",
        "--priority-threshold",
        metavar="THRESHOLD",
        type=int,
        default=None,
        help="(glossary node) exclude entries whose priority > THRESHOLD",
    )
    add_verbose_arguments(dynamic_node_parser)

    dynamic_node_parser.set_defaults(func=_dynamic_node_main)
