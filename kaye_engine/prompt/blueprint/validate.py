"""
validate.py

define ``validate_blueprint``
"""

from .data import Blueprint
from .index import get_corpus_index
from .selection import bind_selection

__all__ = ("validate_blueprint",)


# Public API  ##################################################################
def validate_blueprint(blueprint):
    """
    fail early on what a blueprint cannot render: a dependency name that
    is not registered, and, while a corpus is loaded, a path that is not
    in it


    :param blueprint:
    :type blueprint: Blueprint
    :raises ValueError: an unregistered dependency name, or a path the
            loaded corpus does not contain
    :return: ``blueprint`` itself, unchanged
    :rtype: Blueprint
    """
    from .registry import blueprint_registry  # pylint: disable=C0415

    for dep in blueprint.dependencies:
        if isinstance(dep, Blueprint):
            validate_blueprint(dep)
        elif dep not in blueprint_registry:
            raise ValueError(
                "no blueprint registered under dependency name: {}".format(dep)
            )

    try:
        get_corpus_index()
    except ValueError:
        return blueprint  # no corpus yet: paths are checked when needed

    bind_selection(blueprint)
    return blueprint
