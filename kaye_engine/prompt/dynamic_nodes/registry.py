"""
registry.py

define ``resolve_dynamic_node_factory`` -- the single canonical-name
resolver shared by the corpus loader and the CLI
"""

import functools

from kaye_engine.abbr_collection import abbr_glossary_registry

from .abbr_tag_node import ABBR_TAG_NODE_MEMBERS, AbbrTagNode, slug_for_abbr_tag
from .glossary_node import GlossaryNode

__all__ = ("resolve_dynamic_node_factory",)


def resolve_dynamic_node_factory(name, require_substitution_flag=False):
    """
    resolve a canonical kebab-case ``name`` against ``DYNAMIC_NODE_TYPES``
    first, then ``ABBR_TAG_NODE_MEMBERS``, then against every glossary
    name known to ``abbr_glossary_registry``

    :param name: canonical ``NAME`` slug to resolve
    :type name: str
    :param require_substitution_flag: when True, a glossary name only
            resolves if registered with
            ``register_as_dynamic_substitution=True``; defaults to
            False
    :type require_substitution_flag: bool, optional
    :raises ValueError: ``name`` matches none of the above
    :return: a zero-arg-parametrized callable of signature
            ``factory(parent=None, **kwargs)`` constructing the matched
            dynamic node
    :rtype: type or functools.partial
    """
    from . import DYNAMIC_NODE_TYPES  # local import avoids circular import

    for cls in DYNAMIC_NODE_TYPES:
        if name == cls.NAME:
            return cls

    for abbr_tag in ABBR_TAG_NODE_MEMBERS:
        if name == slug_for_abbr_tag(abbr_tag):
            return functools.partial(AbbrTagNode, abbr_tag=abbr_tag)

    if name in abbr_glossary_registry and (
        not require_substitution_flag
        or abbr_glossary_registry[name].register_as_dynamic_substitution
    ):
        return functools.partial(GlossaryNode, glossary_name=name)

    raise ValueError("unrecognized dynamic node name: {}".format(name))
