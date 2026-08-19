"""
parser.py

define ``register_dynamic_node_parser``
"""

import functools
import sys
from argparse import RawDescriptionHelpFormatter

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.dynamic_node.node_type_choices import (
    list_all_node_type_names,
)
from kaye_engine.cli.render_options_parser import (
    build_render_options_parent_parser,
    resolve_render_options,
)
from kaye_engine.cli.sparseness_parser import SPARSENESS_DESCRIPTION
from kaye_engine.kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)
from kaye_engine.prompt.blueprint.prompt_blueprint import PromptBlueprint
from kaye_engine.prompt.dynamic_nodes import (
    AbbrTagNode,
    GlossaryNode,
    resolve_dynamic_node_factory,
    slug_for_abbr_tag,
)
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

when NODE=decode-only-abbr, reads query content from stdin, optional:

    echo "use an algo to calc the avg" | kaye-engine dynamic-node decode-only-abbr

run to list available NODE values:

    kaye-engine dynamic-node ls

""" + SPARSENESS_DESCRIPTION


def _resolve_node_type(name):
    """
    resolve ``name`` via :func:`resolve_dynamic_node_factory` against
    the canonical kebab ``NAME`` universe -- returns
    ``(node_cls, kwargs)``, where ``kwargs`` is the dict of parameters
    the match needs at construction time (empty for an engine-defined
    choice, ``{"abbr_tag": ...}`` for an AbbrTagNode match,
    ``{"glossary_name": ...}`` for a glossary match); raises
    ``ValueError`` when ``name`` matches none of the above
    """
    factory = resolve_dynamic_node_factory(name)

    if isinstance(factory, functools.partial):
        return factory.func, dict(factory.keywords)

    return factory, {}


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


def _node_name_in(corpus_tree, node_name_arg, node_cls, kwargs):
    """
    :return: the authored "(...)" heading already present as a child of
            ``corpus_tree`` for ``node_name_arg``, else the name of a
            freshly attached ``node_cls`` instance
    :rtype: str
    """
    if node_cls is AbbrTagNode:
        name_text = slug_for_abbr_tag(kwargs["abbr_tag"])
    elif node_cls is GlossaryNode:
        name_text = kwargs["glossary_name"]
    else:
        name_text = node_cls.NAME
    heading = "(" + name_text + ")"

    has_authored_heading = any(
        child.name == heading for child in corpus_tree.children
    )
    if has_authored_heading:
        return heading

    node = node_cls(corpus_tree, **kwargs)
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
            node_cls, kwargs = _resolve_node_type(node_name_arg)
            node_names.append(
                _node_name_in(corpus_tree, node_name_arg, node_cls, kwargs)
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
            **resolve_render_options(args, default_show_comment=False),
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
        parents=[
            build_render_options_parent_parser(
                default_sparseness=DEFAULT_SPARSENESS
            )
        ],
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
