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
from kaye_engine.cli.sparseness_parser import (
    SPARSENESS_DESCRIPTION,
    sparseness_parser,
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

renders a single blueprint merged from every given NODE dynamic node,
result is printed to stdout

when NODE=shorthand, reads query content from stdin, optional:

    echo "use an algo to calc the avg" | kaye-engine dynamic-node shorthand

run to list available NODE values:

    kaye-engine dynamic-node ls

""" + SPARSENESS_DESCRIPTION


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


def _get_shared_corpus_tree():
    """
    :return: the default corpus tree if one is set, else a fresh dummy
            root -- shared as the single ``corpus_tree`` every requested
            NODE is attached to or read from, so their blueprints can merge
    :rtype: PromptCorpusNode
    """
    try:
        return get_default_corpus_tree()
    except ValueError:
        return PromptCorpusNode(_ROOT_NODE_NAME, None, [])


def _node_name_in(corpus_tree, node_name_arg, node_cls, glossary_name):
    """
    :return: the authored "(...)" heading already present as a child of
            ``corpus_tree`` for ``node_name_arg``, else the name of a
            freshly attached ``node_cls`` instance
    :rtype: str
    """
    heading_text = (
        glossary_name if glossary_name is not None else node_cls.HEADING
    )
    heading = "(" + heading_text + ")"

    has_authored_heading = any(
        child.name == heading for child in corpus_tree.children
    )
    if has_authored_heading:
        return heading

    node = (
        node_cls(corpus_tree, glossary_name=glossary_name)
        if glossary_name is not None
        else node_cls(corpus_tree)
    )
    return node.name


def _dynamic_node_main(args):
    set_logging_level_by_namespace(args, logger=logger)

    if args.NODE == ["ls"]:
        for name in list_all_node_type_names():
            print(name)
        return

    corpus_tree = _get_shared_corpus_tree()

    try:
        node_names = []
        for node_name_arg in args.NODE:
            node_cls, glossary_name = _resolve_node_type(node_name_arg)
            node_names.append(
                _node_name_in(
                    corpus_tree, node_name_arg, node_cls, glossary_name
                )
            )

        blueprint = None
        for node_name in node_names:
            node_blueprint = PromptBlueprint.create_from_node(
                node_name, corpus_tree=corpus_tree
            )
            blueprint = (
                node_blueprint
                if blueprint is None
                else blueprint.merge(node_blueprint)
            )
    except ValueError as err:
        logger.error(str(err))
        raise SystemExit(1) from err

    query = sys.stdin.read() if not sys.stdin.isatty() else ""

    try:
        prompt = blueprint.generate_prompt(
            query=query,
            glossary_priority_threshold=args.priority_threshold,
            sparseness=args.sparseness,
        )
    except (TypeError, KeyError, NotImplementedError) as err:
        logger.critical(str(err))
        raise SystemExit(1) from err

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
        parents=[sparseness_parser],
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
