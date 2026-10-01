"""
prompt-bp-dependencies_test.py

Unit Tests (using pytest) for:

- resolve_dependencies()
- trace_dependencies()
"""

import pytest

from kaye_engine.prompt.blueprint.data import Blueprint
from kaye_engine.prompt.blueprint.dependencies import (
    resolve_dependencies,
    trace_dependencies,
)
from kaye_engine.prompt.blueprint.registry import blueprint_registry


def _bp(label, *dependencies):
    return Blueprint(
        nodes=frozenset({(label,)}), dependencies=tuple(dependencies)
    )


@pytest.fixture
def register():
    names = []

    def _register(name, blueprint):
        # direct insert: dependency names may point at later entries, and
        # no corpus is loaded for these tests
        blueprint_registry[name] = type(
            "Entry", (), {"blueprint": blueprint}
        )()
        names.append(name)

    yield _register

    for name in names:
        blueprint_registry.pop(name, None)


class TestResolve:

    def test_no_dependencies(_):
        assert resolve_dependencies(Blueprint()) == ()

    def test_name_becomes_registered_value(_, register):
        dep = _bp("Dep")
        register("test-dep-a", dep)

        assert resolve_dependencies(_bp("Top", "test-dep-a")) == (dep,)

    def test_value_passes_through(_):
        dep = _bp("Dep")

        assert resolve_dependencies(_bp("Top", dep)) == (dep,)

    def test_order_is_kept(_, register):
        first, second = _bp("First"), _bp("Second")
        register("test-dep-first", first)

        out = resolve_dependencies(_bp("Top", second, "test-dep-first"))

        assert out == (second, first)

    def test_is_direct_only(_, register):
        register("test-dep-leaf", _bp("Leaf"))
        mid = _bp("Mid", "test-dep-leaf")

        assert resolve_dependencies(_bp("Top", mid)) == (mid,)

    def test_unknown_name_raises(_):
        with pytest.raises(ValueError, match="no-such-blueprint"):
            resolve_dependencies(_bp("Top", "no-such-blueprint"))


class TestTrace:

    def test_no_dependencies(_):
        assert trace_dependencies(Blueprint()) == ()

    def test_dependencies_come_first(_, register):
        leaf = _bp("Leaf")
        register("test-trace-leaf", leaf)
        mid = _bp("Mid", "test-trace-leaf")
        register("test-trace-mid", mid)

        assert trace_dependencies(_bp("Top", "test-trace-mid")) == (leaf, mid)

    def test_diamond_lists_shared_dependency_once(_, register):
        base = _bp("Base")
        register("test-trace-base", base)
        left = _bp("Left", "test-trace-base")
        right = _bp("Right", "test-trace-base")
        register("test-trace-left", left)
        register("test-trace-right", right)

        out = trace_dependencies(
            _bp("Top", "test-trace-left", "test-trace-right")
        )

        assert out == (base, left, right)

    def test_nested_value_dependencies_are_followed(_):
        leaf = _bp("Leaf")
        mid = _bp("Mid", leaf)

        assert trace_dependencies(_bp("Top", mid)) == (leaf, mid)

    def test_self_is_excluded(_):
        top = _bp("Top")

        assert top not in trace_dependencies(top)

    def test_cycle_raises(_, register):
        register("test-trace-a", _bp("A", "test-trace-b"))
        register("test-trace-b", _bp("B", "test-trace-a"))

        with pytest.raises(ValueError, match="cycle"):
            trace_dependencies(_bp("Top", "test-trace-a"))

    def test_unknown_name_raises(_):
        with pytest.raises(ValueError, match="no-such-blueprint"):
            trace_dependencies(_bp("Top", "no-such-blueprint"))
