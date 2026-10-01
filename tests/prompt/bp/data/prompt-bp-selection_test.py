"""
prompt-bp-selection_test.py

Unit Tests (using pytest) for:

bind_selection, resolve_selection
"""

from types import SimpleNamespace

import pytest

from kaye_engine.prompt.blueprint.data import Blueprint, create_blueprint
from kaye_engine.prompt.blueprint.edit import checkmark_nodes
from kaye_engine.prompt.blueprint.index import get_corpus_index
from kaye_engine.prompt.blueprint.registry import blueprint_registry
from kaye_engine.prompt.blueprint.selection import (
    bind_selection,
    resolve_selection,
)
from kaye_engine.prompt.prompt_corpus_loader import (
    clear_corpus_tree,
    load_corpus_tree,
)

_SOURCE = """# Main
## Intro
### Background
### {description}
Desc.
## Methods
### Data
# Conclusion
"""

MAIN = ("Main",)
INTRO = ("Main", "Intro")
BACK = ("Main", "Intro", "Background")
DESC = ("Main", "Intro", "{description}")
METHODS = ("Main", "Methods")
DATA = ("Main", "Methods", "Data")
CONCLUSION = ("Conclusion",)


# pytest fixtures  #############################################################
@pytest.fixture(autouse=True)
def corpus():
    load_corpus_tree([_SOURCE])


@pytest.fixture
def registry():
    added = []

    def add(name, blueprint):
        blueprint_registry[name] = SimpleNamespace(blueprint=blueprint)
        added.append(name)

    yield add

    for name in added:
        blueprint_registry.pop(name, None)


def _bits(selection):
    index = selection.index
    return {
        index.paths[i]
        for i in range(len(index.paths))
        if selection.mask >> i & 1
    }


# pytest  ######################################################################
class TestBind:

    def test_nodes(_):
        bp = Blueprint(nodes=frozenset({INTRO, DATA}))

        assert _bits(bind_selection(bp)) == {INTRO, DATA}

    def test_empty(_):
        assert bind_selection(Blueprint()).mask == 0

    def test_subtree_selects_descendants(_):
        bp = checkmark_nodes(create_blueprint(), INTRO, is_recursive=True)

        assert _bits(bind_selection(bp)) == {INTRO, BACK}

    def test_subtree_excludes_sidecars(_):
        bp = checkmark_nodes(create_blueprint(), MAIN, is_recursive=True)

        assert DESC not in _bits(bind_selection(bp))

    def test_explicit_sidecar_node_is_selected(_):
        bp = Blueprint(nodes=frozenset({DESC}))

        assert _bits(bind_selection(bp)) == {DESC}

    def test_full_blueprint_selects_every_non_sidecar_except_root(_):
        bits = _bits(bind_selection(create_blueprint(is_full=True)))
        index = get_corpus_index()

        assert () not in bits
        assert DESC not in bits
        assert {MAIN, INTRO, BACK, METHODS, DATA, CONCLUSION} <= bits
        assert len(bits) == len(index.paths) - 1 - 1

    def test_node_added_under_subtree_is_selected(_):
        # a stored subtree means "everything under here, as the corpus has
        # it now": a different corpus yields a different selection
        bp = checkmark_nodes(create_blueprint(), INTRO, is_recursive=True)
        before = _bits(bind_selection(bp))

        clear_corpus_tree()
        load_corpus_tree([_SOURCE.replace("### {description}", "### New")])
        after = _bits(bind_selection(bp))

        assert before == {INTRO, BACK}
        assert after == {INTRO, BACK, ("Main", "Intro", "New")}

    def test_unknown_path_raises_naming_it(_):
        bp = Blueprint(nodes=frozenset({("Main", "Nope")}))

        with pytest.raises(ValueError, match="Nope"):
            bind_selection(bp)

    def test_unknown_subtree_path_raises(_):
        bp = Blueprint(subtrees=frozenset({("Nope",)}))

        with pytest.raises(ValueError, match="Nope"):
            bind_selection(bp)

    def test_memoized(_):
        bp = Blueprint(nodes=frozenset({INTRO}))

        assert bind_selection(bp) is bind_selection(bp)
        assert bind_selection(bp) is bind_selection(
            Blueprint(nodes=frozenset({INTRO}))
        )

    def test_memo_cleared_with_corpus(_):
        bp = Blueprint(nodes=frozenset({INTRO}))
        first = bind_selection(bp)

        clear_corpus_tree()
        load_corpus_tree([_SOURCE])

        assert bind_selection(bp) is not first

    def test_dependencies_not_bound(_, registry):
        registry("dep", Blueprint(nodes=frozenset({DATA})))
        bp = Blueprint(nodes=frozenset({INTRO}), dependencies=("dep",))

        assert _bits(bind_selection(bp)) == {INTRO}


class TestResolve:

    def test_no_dependencies_equals_bind(_):
        bp = Blueprint(nodes=frozenset({INTRO}))

        assert resolve_selection(bp).mask == bind_selection(bp).mask

    def test_name_dependency(_, registry):
        registry("dep", Blueprint(nodes=frozenset({DATA})))
        bp = Blueprint(nodes=frozenset({INTRO}), dependencies=("dep",))

        assert _bits(resolve_selection(bp)) == {INTRO, DATA}

    def test_late_binding(_, registry):
        bp = Blueprint(nodes=frozenset({INTRO}), dependencies=("later",))

        with pytest.raises(ValueError, match="later"):
            resolve_selection(bp)

        registry("later", Blueprint(nodes=frozenset({CONCLUSION})))

        assert _bits(resolve_selection(bp)) == {INTRO, CONCLUSION}

    def test_replaced_dependency_is_seen(_, registry):
        registry("dep", Blueprint(nodes=frozenset({DATA})))
        bp = Blueprint(dependencies=("dep",))
        assert _bits(resolve_selection(bp)) == {DATA}

        registry("dep", Blueprint(nodes=frozenset({METHODS})))

        assert _bits(resolve_selection(bp)) == {METHODS}

    def test_transitive(_, registry):
        registry("c", Blueprint(nodes=frozenset({DATA})))
        registry("b", Blueprint(nodes=frozenset({BACK}), dependencies=("c",)))
        bp = Blueprint(nodes=frozenset({INTRO}), dependencies=("b",))

        assert _bits(resolve_selection(bp)) == {INTRO, BACK, DATA}

    def test_nested_value_dependency(_):
        inner = Blueprint(nodes=frozenset({DATA}))
        bp = Blueprint(nodes=frozenset({INTRO}), dependencies=(inner,))

        assert _bits(resolve_selection(bp)) == {INTRO, DATA}

    def test_diamond_is_not_a_cycle(_, registry):
        registry("shared", Blueprint(nodes=frozenset({DATA})))
        registry("l", Blueprint(dependencies=("shared",)))
        registry("r", Blueprint(dependencies=("shared",)))
        bp = Blueprint(dependencies=("l", "r"))

        assert _bits(resolve_selection(bp)) == {DATA}

    def test_cycle_raises(_, registry):
        registry("a", Blueprint(dependencies=("b",)))
        registry("b", Blueprint(dependencies=("a",)))

        with pytest.raises(ValueError, match="dependency cycle"):
            resolve_selection(Blueprint(dependencies=("a",)))

    def test_self_cycle_raises(_, registry):
        registry("a", Blueprint(dependencies=("a",)))

        with pytest.raises(ValueError, match="dependency cycle"):
            resolve_selection(Blueprint(dependencies=("a",)))

    def test_unknown_name_raises(_):
        with pytest.raises(ValueError, match="ghost"):
            resolve_selection(Blueprint(dependencies=("ghost",)))
