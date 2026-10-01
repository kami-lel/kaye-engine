"""
data.py

define ``Blueprint``, ``BlueprintMeta``, ``create_blueprint``, and the
JSON codec ``encode_blueprint``, ``decode_blueprint``, ``load_blueprint``,
``save_blueprint`` -- a blueprint is pure frozen data, touching no corpus
"""

import json
from dataclasses import dataclass
from pathlib import Path

from .index import NodePath

__all__ = (
    "BLUEPRINT_SCHEMA",
    "Blueprint",
    "BlueprintMeta",
    "create_blueprint",
    "decode_blueprint",
    "encode_blueprint",
    "load_blueprint",
    "save_blueprint",
)

# schema number carried on the envelope of an encoded blueprint
BLUEPRINT_SCHEMA = 1

_META_PATH_FIELDS = ("description_node", "when_to_use_node", "globs_node")


@dataclass(frozen=True, slots=True, kw_only=True)
class BlueprintMeta:  ##########################################################
    """
    descriptors of a blueprint, replacing sidecar lookups


    :param description: literal description, taking priority over the
            description node; defaults to None
    :type description: str, optional
    :param description_node: path of the node holding the description
    :type description_node: NodePath, optional
    :param when_to_use_node: path of the node holding the when-to-use
    :type when_to_use_node: NodePath, optional
    :param globs_node: path of the node holding the glob patterns
    :type globs_node: NodePath, optional
    """

    description: str | None = None
    description_node: NodePath | None = None
    when_to_use_node: NodePath | None = None
    globs_node: NodePath | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class Blueprint:  ##############################################################
    """
    an immutable selection of corpus nodes


    :param meta: descriptors
    :type meta: BlueprintMeta, optional
    :param nodes: paths of nodes checkmarked one by one
    :type nodes: frozenset[NodePath], optional
    :param subtrees: paths of nodes checkmarked together with every
            descendant, expanded when the blueprint is bound
    :type subtrees: frozenset[NodePath], optional
    :param dependencies: a ``str`` names a registered blueprint, resolved
            at render time; a ``Blueprint`` is carried as a value
    :type dependencies: tuple[str or Blueprint, ...], optional
    """

    meta: BlueprintMeta = BlueprintMeta()
    nodes: frozenset[NodePath] = frozenset()
    subtrees: frozenset[NodePath] = frozenset()
    dependencies: tuple["str | Blueprint", ...] = ()


# auxiliaries  #################################################################
def _encode_path(path):
    return list(path)


def _decode_path(raw, where):
    if not isinstance(raw, (list, tuple)) or not all(
        isinstance(name, str) for name in raw
    ):
        raise ValueError(
            "{} must be a list of node names: {}".format(where, repr(raw))
        )
    return tuple(raw)


def _encode_paths(paths):
    return [_encode_path(path) for path in sorted(paths)]


def _encode_body(blueprint):
    meta = {"description": blueprint.meta.description}
    for field in _META_PATH_FIELDS:
        value = getattr(blueprint.meta, field)
        if value is not None:
            meta[field] = _encode_path(value)

    return {
        "meta": meta,
        "nodes": _encode_paths(blueprint.nodes),
        "subtrees": _encode_paths(blueprint.subtrees),
        "dependencies": [
            dep if isinstance(dep, str) else _encode_body(dep)
            for dep in blueprint.dependencies
        ],
    }


def _decode_body(data):
    if not isinstance(data, dict):
        raise ValueError("blueprint must be an object: {}".format(repr(data)))

    raw_meta = data.get("meta") or {}
    meta_kwargs = {}
    description = raw_meta.get("description")
    if description is not None and not isinstance(description, str):
        raise ValueError("meta.description must be a string or null")
    meta_kwargs["description"] = description
    for field in _META_PATH_FIELDS:
        raw = raw_meta.get(field)
        if raw is not None:
            meta_kwargs[field] = _decode_path(raw, "meta." + field)

    dependencies = []
    for raw in data.get("dependencies") or ():
        dependencies.append(raw if isinstance(raw, str) else _decode_body(raw))

    return Blueprint(
        meta=BlueprintMeta(**meta_kwargs),
        nodes=frozenset(
            _decode_path(raw, "nodes entry") for raw in data.get("nodes") or ()
        ),
        subtrees=frozenset(
            _decode_path(raw, "subtrees entry")
            for raw in data.get("subtrees") or ()
        ),
        dependencies=tuple(dependencies),
    )


# Public API  ##################################################################
def create_blueprint(*, meta=None, dependencies=(), is_full=False):
    """
    :param meta: descriptors; defaults to none set
    :type meta: BlueprintMeta, optional
    :param dependencies: registered blueprint names or blueprint values
    :type dependencies: Iterable[str or Blueprint], optional
    :param is_full: whether to select the whole corpus, as a single
            ``subtrees`` entry for root; sidecars are never selected
            that way
    :type is_full: bool, optional
    :return: a new blueprint, empty unless ``is_full``
    :rtype: Blueprint
    """
    return Blueprint(
        meta=meta if meta is not None else BlueprintMeta(),
        subtrees=frozenset({()}) if is_full else frozenset(),
        dependencies=tuple(dependencies),
    )


def encode_blueprint(blueprint):
    """
    :param blueprint: blueprint to encode
    :type blueprint: Blueprint
    :return: JSON-ready form with the schema number on the envelope;
            paths sorted, so equal blueprints encode identically
    :rtype: dict
    """
    return {"schema": BLUEPRINT_SCHEMA, **_encode_body(blueprint)}


def decode_blueprint(data):
    """
    pure data: touches no corpus, so it may run before one is loaded


    :param data: the form :func:`encode_blueprint` returns, or its JSON
            text
    :type data: dict or str
    :raises ValueError: malformed JSON, unknown schema number, or a
            malformed field
    :return: the decoded blueprint
    :rtype: Blueprint
    """
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as err:
            raise ValueError("blueprint is not valid JSON") from err

    if not isinstance(data, dict):
        raise ValueError("blueprint must be an object: {}".format(repr(data)))

    schema = data.get("schema")
    if schema != BLUEPRINT_SCHEMA:
        raise ValueError(
            "unsupported blueprint schema {}, expected {}".format(
                repr(schema), BLUEPRINT_SCHEMA
            )
        )

    return _decode_body(data)


def load_blueprint(file_path):
    """
    :param file_path: JSON file holding an encoded blueprint
    :type file_path: str or Path
    :raises ValueError: see :func:`decode_blueprint`
    :raises FileNotFoundError:
    :return: the decoded blueprint
    :rtype: Blueprint
    """
    return decode_blueprint(Path(file_path).read_text(encoding="utf-8"))


def save_blueprint(blueprint, file_path):
    """
    :param blueprint: blueprint to write
    :type blueprint: Blueprint
    :param file_path: JSON file to write
    :type file_path: str or Path
    """
    Path(file_path).write_text(
        json.dumps(encode_blueprint(blueprint), indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
