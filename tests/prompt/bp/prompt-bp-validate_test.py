"""
prompt-bp-validate_test.py

Unit Tests (using pytest) for:

- validate_blueprint()
"""

import pytest

from kaye_engine.prompt.blueprint.data import Blueprint, create_blueprint
from kaye_engine.prompt.blueprint.registry import (
    blueprint_registry,
    register_blueprint,
)
from kaye_engine.prompt.blueprint.validate import validate_blueprint
from kaye_engine.prompt.prompt_corpus_loader import (
    clear_corpus_tree,
    load_corpus_tree,
)


@pytest.fixture(autouse=True)
def no_corpus():
    clear_corpus_tree()
    yield
    clear_corpus_tree()


class TestStructure:

    def test_returns_same_blueprint(_):
        bp = Blueprint(nodes=frozenset({("A",)}))

        assert validate_blueprint(bp) is bp

    def test_empty_blueprint_is_valid(_):
        bp = create_blueprint()

        assert validate_blueprint(bp) is bp


class TestDependencies:

    def test_unknown_name_raises(_):
        bp = create_blueprint(dependencies=["no-such-blueprint"])

        with pytest.raises(ValueError, match="no-such-blueprint"):
            validate_blueprint(bp)

    def test_unknown_name_in_nested_value_raises(_):
        inner = Blueprint(dependencies=("no-such-blueprint",))

        with pytest.raises(ValueError, match="no-such-blueprint"):
            validate_blueprint(Blueprint(dependencies=(inner,)))

    def test_registered_name_is_accepted(_):
        register_blueprint(
            "test-validate-dep",
            create_blueprint(),
            display_name="Dep",
            is_exportable=False,
        )
        try:
            bp = create_blueprint(dependencies=["test-validate-dep"])

            assert validate_blueprint(bp) is bp
        finally:
            blueprint_registry.pop("test-validate-dep", None)


class TestPaths:

    def test_unknown_path_raises_while_corpus_loaded(_):
        load_corpus_tree(["# A\n"])
        bp = Blueprint(nodes=frozenset({("A", "Nope")}))

        with pytest.raises(ValueError, match="Nope"):
            validate_blueprint(bp)

    def test_known_path_is_accepted(_):
        load_corpus_tree(["# A\n"])
        bp = Blueprint(nodes=frozenset({("A",)}))

        assert validate_blueprint(bp) is bp

    def test_paths_unchecked_without_corpus(_):
        bp = Blueprint(nodes=frozenset({("Anything",)}))

        assert validate_blueprint(bp) is bp
