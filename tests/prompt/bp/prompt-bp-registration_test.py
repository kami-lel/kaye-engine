"""
prompt-bp-registration_test.py

Unit Tests (using pytest) for the registration helpers:

- bind_registrars()
- register_node(), register_leaf()
- mark_as_leaf(), walk_and_checkmark()
- glossary_blueprint()
- register_md_file_dynamic_substitution()
"""

import pytest

from kaye_engine.abbr_collection.abbr_glossary_registry import (
    abbr_glossary_registry,
)
from kaye_engine.consumer import register_consumer
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import (
    get_corpus_node,
    is_checkmarked,
)
from kaye_engine.prompt.blueprint.dynamic_substitution import (
    dynamic_substitution_registry,
)
from kaye_engine.prompt.blueprint.registry import blueprint_registry
from kaye_engine.prompt.prompt_corpus_loader import clear_corpus_tree
from kaye_engine.registration import (
    bind_registrars,
    glossary_blueprint,
    mark_as_leaf,
    register_leaf,
    register_md_file_dynamic_substitution,
    register_node,
    walk_and_checkmark,
)

from tests.consumer_helper import isolated_consumers
from tests.corpus_helper import load_corpus_from_sources

_CORPUS = """# Root

## Group

### Leaf

leaf body

#### {description}

the leaf description

### Other

other body

## Solo

solo body

# (my-gloss)

- a:alpha
"""

_PREFIX = "reg-test-"


@pytest.fixture(autouse=True)
def _corpus():
    clear_corpus_tree()
    with isolated_consumers():
        register_consumer("Reg Pkg", "reg-pkg", "1.0.0")
        bind_registrars("reg-pkg").register_abbr_glossary(
            "my-gloss", is_exportable=False
        )
        load_corpus_from_sources([_CORPUS])
        yield
    abbr_glossary_registry.pop("my-gloss", None)
    for name in [n for n in blueprint_registry if n.startswith(_PREFIX)]:
        blueprint_registry.pop(name, None)
        exportable_registry.pop(name, None)
    clear_corpus_tree()


class TestBindRegistrars:

    def test_exportable_owned_by_consumer(_):
        reg = bind_registrars("reg-pkg")
        node = get_corpus_node("Root")

        entry = register_node(
            reg.register_exportable, _PREFIX + "a", node, "Solo"
        )

        assert entry.consumer == "reg-pkg"
        assert entry.is_exportable is True
        assert exportable_registry[_PREFIX + "a"] is entry

    def test_prompt_is_exportable_not_llm_invokable(_):
        reg = bind_registrars("reg-pkg")
        node = get_corpus_node("Root")

        entry = register_node(
            reg.register_prompt, _PREFIX + "b", node, "Solo"
        )

        assert entry.is_exportable is True
        assert entry.llm_invokable is False
        assert entry.consumer == "reg-pkg"

    def test_internal_is_not_exported(_):
        reg = bind_registrars("reg-pkg")
        node = get_corpus_node("Root")

        entry = register_node(
            reg.register_internal, _PREFIX + "c", node, "Solo"
        )

        assert entry.is_exportable is False
        assert _PREFIX + "c" not in exportable_registry

    def test_abbr_glossary_owned_by_consumer(_):
        assert abbr_glossary_registry["my-gloss"].consumer == "reg-pkg"

    def test_named_fields(_):
        reg = bind_registrars("reg-pkg")

        assert reg.register_exportable is reg[0]
        assert reg.register_abbr_glossary is reg[3]

    def test_keyword_overridable(_):
        reg = bind_registrars("reg-pkg")
        node = get_corpus_node("Root")

        entry = register_node(
            reg.register_exportable,
            _PREFIX + "d",
            node,
            "Solo",
            always_apply=True,
        )

        assert entry.always_apply is True


class TestRegisterNode:

    def test_display_name_defaults_to_node_name(_):
        reg = bind_registrars("reg-pkg")

        entry = register_node(
            reg.register_internal,
            _PREFIX + "n1",
            get_corpus_node("Root"),
            "Solo",
        )

        assert entry.display_name == "Solo"

    def test_display_name_and_description_set(_):
        reg = bind_registrars("reg-pkg")

        entry = register_node(
            reg.register_internal,
            _PREFIX + "n2",
            get_corpus_node("Root"),
            "Solo",
            display_name="Alone",
            description="only one",
        )

        assert entry.display_name == "Alone"
        assert entry.blueprint.meta.description == "only one"

    def test_recursive_takes_subtree(_):
        reg = bind_registrars("reg-pkg")
        group = get_corpus_node("Root")["Group"]

        entry = register_node(
            reg.register_internal,
            _PREFIX + "n3",
            get_corpus_node("Root"),
            "Group",
            recursively=True,
        )

        assert is_checkmarked(entry.blueprint, group["Leaf"])
        assert is_checkmarked(entry.blueprint, group["Other"])

    def test_non_recursive_takes_node_alone(_):
        reg = bind_registrars("reg-pkg")
        group = get_corpus_node("Root")["Group"]

        entry = register_node(
            reg.register_internal,
            _PREFIX + "n4",
            get_corpus_node("Root"),
            "Group",
        )

        assert is_checkmarked(entry.blueprint, group)
        assert not is_checkmarked(entry.blueprint, group["Leaf"])

    def test_dependencies_kept(_):
        reg = bind_registrars("reg-pkg")
        root = get_corpus_node("Root")
        register_node(reg.register_internal, _PREFIX + "base", root, "Solo")

        entry = register_node(
            reg.register_internal,
            _PREFIX + "n5",
            root,
            "Group",
            dependencies=[_PREFIX + "base"],
        )

        assert entry.blueprint.dependencies == (_PREFIX + "base",)


class TestLeaf:

    def test_walk_and_checkmark_marks_each_ancestor(_):
        from kaye_engine.prompt.blueprint import create_blueprint

        bp, path = walk_and_checkmark(create_blueprint(), ["Root", "Group"])

        assert path == ("Root", "Group")
        assert is_checkmarked(bp, get_corpus_node("Root"))
        assert is_checkmarked(bp, get_corpus_node("Root")["Group"])
        assert not is_checkmarked(
            bp, get_corpus_node("Root")["Group"]["Leaf"]
        )

    def test_mark_as_leaf_points_meta_at_description(_):
        from kaye_engine.prompt.blueprint import create_blueprint

        bp = mark_as_leaf(create_blueprint(), ("Root", "Group", "Leaf"))

        assert bp.meta.description_node == (
            "Root",
            "Group",
            "Leaf",
            "{description}",
        )
        assert bp.meta.when_to_use_node is None

    def test_register_leaf_takes_leaf_under_ancestors(_):
        reg = bind_registrars("reg-pkg")
        group = get_corpus_node("Root")["Group"]

        entry = register_leaf(
            reg.register_exportable,
            _PREFIX + "l1",
            ["Root", "Group"],
            "Leaf",
        )

        assert entry.display_name == "Leaf"
        assert is_checkmarked(entry.blueprint, group)
        assert is_checkmarked(entry.blueprint, group["Leaf"])
        assert not is_checkmarked(entry.blueprint, group["Other"])

    def test_register_leaf_description_literal(_):
        reg = bind_registrars("reg-pkg")

        entry = register_leaf(
            reg.register_exportable,
            _PREFIX + "l2",
            ["Root", "Group"],
            "Leaf",
            description="own words",
        )

        assert entry.blueprint.meta.description == "own words"


class TestGlossaryBlueprint:

    def test_checkmarks_each_named_glossary(_):
        bp = glossary_blueprint("my-gloss")

        assert is_checkmarked(bp, get_corpus_node("(my-gloss)"))


class TestMdFileSubstitution:

    def test_registers_file_text(_, tmp_path):
        path = tmp_path / "sub.md"
        path.write_text("hello substitution")
        name = _PREFIX + "sub"
        try:
            register_md_file_dynamic_substitution(
                name, path, logger_name="reg-test"
            )

            assert (
                dynamic_substitution_registry[name].generate()
                == "hello substitution"
            )
        finally:
            dynamic_substitution_registry.pop(name, None)

    def test_unreadable_file_exits_1(_, tmp_path):
        with pytest.raises(SystemExit) as info:
            register_md_file_dynamic_substitution(
                _PREFIX + "missing",
                tmp_path / "absent.md",
                logger_name="reg-test",
            )

        assert info.value.code == 1
