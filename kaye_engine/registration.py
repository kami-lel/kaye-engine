"""
kaye_engine/registration.py

registration helpers a consumer builds its blueprints with: the
consumer-bound registrars of :func:`bind_registrars`, and the node, leaf
and glossary shortcuts every registration repeats

※ `Registration Helpers <../docs/prompt-doc.md#registration-helpers>`__
"""

import functools
from typing import Callable, NamedTuple

import kamilog

from kaye_engine.abbr_collection import register_abbr_glossary as _register_abbr
from kaye_engine.prompt.blueprint import (
    StringDynamicSubstitution,
    checkmark_nodes,
    create_blueprint,
    create_blueprint_from_node,
    get_corpus_index,
    register_blueprint,
    register_dynamic_substitution,
    replace_meta,
)

__all__ = (
    "Registrars",
    "bind_registrars",
    "glossary_blueprint",
    "mark_as_leaf",
    "register_leaf",
    "register_md_file_dynamic_substitution",
    "register_node",
    "walk_and_checkmark",
)


class Registrars(NamedTuple):
    """
    the registration functions bound to one consumer, from
    :func:`bind_registrars`; each forwards to ``register_blueprint`` or
    ``register_abbr_glossary``, its other keyword arguments overridable
    """

    register_exportable: Callable
    """an exportable skill, the consumer's plugin holding it"""
    register_prompt: Callable
    """an exportable the assistant never brings in on its own judgment"""
    register_internal: Callable
    """a building block, never exported"""
    register_abbr_glossary: Callable
    """an abbreviation glossary owned by the consumer"""


def bind_registrars(consumer):
    """
    bind the registration functions to ``consumer``, so a package spells
    its owner once


    :param consumer: canonical name of the registered consumer owning
            every exportable the registrars create
    :type consumer: str
    :return: the bound ``register_exportable``, ``register_prompt``,
            ``register_internal`` and ``register_abbr_glossary``
    :rtype: Registrars
    :example:
    >>> (
    ...     register_exportable,
    ...     register_prompt,
    ...     register_internal,
    ...     register_abbr_glossary,
    ... ) = bind_registrars("my-consumer")
    """
    return Registrars(
        register_exportable=functools.partial(
            register_blueprint, is_exportable=True, consumer=consumer
        ),
        register_prompt=functools.partial(
            register_blueprint,
            is_exportable=True,
            llm_invokable=False,
            consumer=consumer,
        ),
        register_internal=functools.partial(
            register_blueprint, is_exportable=False
        ),
        register_abbr_glossary=functools.partial(
            _register_abbr, consumer=consumer
        ),
    )


def register_node(
    register_fn,
    slug,
    container,
    name,
    *,
    recursively=False,
    dependencies=None,
    display_name=None,
    description=None,
    **extra,
):
    """
    register the node ``name`` of ``container`` under ``slug``


    :param register_fn: registrar the blueprint goes through, eg a
            :func:`bind_registrars` one
    :type register_fn: Callable
    :param slug: canonical name to register under
    :type slug: str
    :param container: corpus node holding the node ``name``
    :type container: PromptCorpusNode
    :param name: name of the node to register
    :type name: str
    :param recursively: whether to take the node's whole subtree
    :type recursively: bool, optional
    :param dependencies: blueprints, by name or object, the new one
            depends on
    :type dependencies: list, optional
    :param display_name: display name; defaults to ``name``
    :type display_name: str, optional
    :param description: literal description, over the node's own
            ``{description}`` sidecar
    :type description: str, optional
    :param extra: further keyword arguments for ``register_fn``
    :return: the created registry entry
    :rtype: BlueprintRegistry
    """
    bp = create_blueprint_from_node(
        container[name],
        is_recursive=recursively,
        dependencies=dependencies or (),
    )
    bp = replace_meta(bp, display_name=display_name or name)
    if description is not None:
        bp = replace_meta(bp, description=description)

    return register_fn(slug, bp, **extra)


def walk_and_checkmark(bp, ancestor_path):
    """
    walk ``ancestor_path``, checkmarking each node non-recursively


    :param bp: blueprint to checkmark the path in
    :type bp: Blueprint
    :param ancestor_path: node names from the root down
    :type ancestor_path: Sequence[str]
    :return: the blueprint with every node on the path checkmarked, and
            the path of the last one
    :rtype: tuple[Blueprint, tuple[str, ...]]
    """
    path = ()
    for name in ancestor_path:
        path = (*path, name)
        bp = checkmark_nodes(bp, path)
    return bp, path


def mark_as_leaf(bp, leaf_path):
    """
    checkmark the node at ``leaf_path`` recursively, and point the
    blueprint's meta at the leaf's own ``{description}``,
    ``{when_to_use}`` and ``{globs}`` sidecar nodes, where it has them


    :param bp: blueprint to mark the leaf in
    :type bp: Blueprint
    :param leaf_path: path of the leaf node
    :type leaf_path: tuple[str, ...]
    :return: the blueprint with the leaf and its descriptors marked
    :rtype: Blueprint
    """
    index = get_corpus_index()

    bp = checkmark_nodes(bp, leaf_path, is_recursive=True)

    descriptors = {}
    for field, name in (
        ("description_node", "{description}"),
        ("when_to_use_node", "{when_to_use}"),
        ("globs_node", "{globs}"),
    ):
        path = (*leaf_path, name)
        if path in index.idx_by_path:
            descriptors[field] = path

    return replace_meta(bp, **descriptors)


def register_leaf(
    register_fn,
    slug,
    ancestor_path,
    leaf_name,
    *,
    display_name=None,
    description=None,
    dependencies=None,
    extra_checkmarks=(),
    **extra,
):
    """
    register ``leaf_name`` under the node at ``ancestor_path``: every
    ancestor heading alone, then the leaf's whole subtree and its
    descriptors


    :param register_fn: registrar the blueprint goes through
    :type register_fn: Callable
    :param slug: canonical name to register under
    :type slug: str
    :param ancestor_path: node names from the root down to the leaf's
            parent
    :type ancestor_path: Sequence[str]
    :param leaf_name: name of the leaf node
    :type leaf_name: str
    :param display_name: display name; defaults to ``leaf_name``
    :type display_name: str, optional
    :param description: literal description, over the leaf's own
            ``{description}`` sidecar
    :type description: str, optional
    :param dependencies: blueprints, by name or object, the new one
            depends on
    :type dependencies: list, optional
    :param extra_checkmarks: further root-level node names to checkmark
    :type extra_checkmarks: Sequence[str], optional
    :param extra: further keyword arguments for ``register_fn``
    :return: the created registry entry
    :rtype: BlueprintRegistry
    """
    bp = create_blueprint(dependencies=dependencies or ())
    bp, ancestor_path = walk_and_checkmark(bp, ancestor_path)

    for extra_node_name in extra_checkmarks:
        bp = checkmark_nodes(bp, (extra_node_name,))

    bp = mark_as_leaf(bp, (*ancestor_path, leaf_name))

    bp = replace_meta(bp, display_name=display_name or leaf_name)
    if description is not None:
        bp = replace_meta(bp, description=description)

    return register_fn(slug, bp, **extra)


def glossary_blueprint(*glossary_names):
    """
    build a blueprint checkmarking the dynamic node ``(name)`` of each of
    ``glossary_names``


    :return: the blueprint selecting every named glossary node
    :rtype: Blueprint
    """
    bp = create_blueprint()
    for name in glossary_names:
        bp = checkmark_nodes(bp, f"({name})")
    return bp


def register_md_file_dynamic_substitution(name, md_file_path, *, logger_name):
    """
    register the text of ``md_file_path`` as the
    ``StringDynamicSubstitution`` ``name``


    :param name: substitution name, spliced by ``(((name)))``
    :type name: str
    :param md_file_path: file whose text is the substitution
    :type md_file_path: Path
    :param logger_name: logger a read failure reports through, so a
            consumer logs under its own name
    :type logger_name: str
    :raises SystemExit: the file cannot be read
    """
    try:
        content = md_file_path.read_text()
    except OSError as err:
        kamilog.getLogger(logger_name).critical(
            f"cannot read {name} file {md_file_path}:\t" + str(err)
        )
        raise SystemExit(1) from err

    register_dynamic_substitution(name, StringDynamicSubstitution(content))
