"""
aux_input.py

define ``LoadedBlueprint``, ``read_stdin_str``, ``detect_str_fmt``,
``parse_str_blueprint``, ``get_name_blueprint``, ``get_cmd_blueprint`` --
the CLI glue that turns ``BLUEPRINT`` (a name, or stdin) into a
`Blueprint`; format detection lives here, never in the API
"""

import sys
from typing import NamedTuple

from kaye_engine.prompt.blueprint import (
    Blueprint,
    blueprint_registry,
    parse_blueprint_json,
    parse_blueprint_tree,
)

__all__ = (
    "LoadedBlueprint",
    "detect_str_fmt",
    "get_cmd_blueprint",
    "get_name_blueprint",
    "parse_str_blueprint",
    "read_stdin_str",
)

# constants  ###################################################################
STDIN_DISPLAY_NAME = "<stdin>"


class LoadedBlueprint(NamedTuple):
    """
    a blueprint as the CLI received it


    :param blueprint: the blueprint itself
    :type blueprint: Blueprint
    :param display_name: the registry entry's display name, or ``"<stdin>"``
    :type display_name: str
    :param registry: the entry the blueprint was looked up from, ``None``
            when read from stdin
    :type registry: BlueprintRegistry or None
    """

    blueprint: Blueprint
    display_name: str
    registry: object


# auxiliaries  #################################################################
def _get_name_entry(name):
    """
    :raises ValueError: no blueprint is registered under ``name``
    :return: the registry entry
    :rtype: BlueprintRegistry
    """
    try:
        return blueprint_registry[name]
    except KeyError as err:
        raise ValueError("unknown blueprint: {}".format(name)) from err


# Public API  ##################################################################
def read_stdin_str():
    """
    :raises ValueError: stdin is a terminal, where reading would hang
    :return: everything on stdin
    :rtype: str
    """
    if sys.stdin.isatty():
        raise ValueError(
            "no BLUEPRINT given and stdin is a terminal: "
            "pass a name, or pipe a blueprint in"
        )

    return sys.stdin.read()


def detect_str_fmt(text):
    """
    :param text: blueprint text
    :type text: str
    :return: ``"json"`` if the first non-blank char is ``{``, otherwise
            ``"tree"``
    :rtype: str
    """
    stripped = text.lstrip()

    return "json" if stripped.startswith("{") else "tree"


def parse_str_blueprint(text):
    """
    :param text: blueprint as JSON or as a preview tree
    :type text: str
    :raises ValueError: see :func:`parse_blueprint_json` and
            :func:`parse_blueprint_tree`
    :return: the parsed blueprint
    :rtype: Blueprint
    """
    if detect_str_fmt(text) == "json":
        return parse_blueprint_json(text)

    return parse_blueprint_tree(text)


def get_name_blueprint(name):
    """
    :param name: registered blueprint name
    :type name: str
    :raises ValueError: no blueprint is registered under ``name``
    :return: the registered blueprint
    :rtype: Blueprint
    """
    return _get_name_entry(name).blueprint


def get_cmd_blueprint(name):
    """
    :param name: registered blueprint name, ``None`` to read stdin
    :type name: str or None
    :raises ValueError: an unknown name, a terminal on stdin, or a
            blueprint text that does not parse
    :return: the blueprint with its display name and registry entry
    :rtype: LoadedBlueprint
    """
    if name is None:
        return LoadedBlueprint(
            parse_str_blueprint(read_stdin_str()), STDIN_DISPLAY_NAME, None
        )

    entry = _get_name_entry(name)

    return LoadedBlueprint(entry.blueprint, entry.display_name, entry)
