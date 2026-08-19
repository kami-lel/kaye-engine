"""
prompt-bp-registry_test.py

Unit Tests (using pytest) for:

- register_blueprint()
- BlueprintRegistry
"""

import pytest

from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import PromptBlueprint
from kaye_engine.prompt.blueprint.registry import (
    BlueprintRegistry,
    register_blueprint,
    blueprint_registry,
)


@pytest.fixture
def registered_names():
    names = []
    yield names
    for name in names:
        blueprint_registry.pop(name, None)
        exportable_registry.pop(name, None)


class TestRegisterBlueprint:  ###################################################

    def test_dft(_, corpus_testee1, registered_names):
        bp = PromptBlueprint.create_empty_blueprint(
            corpus_tree=corpus_testee1
        )

        reg = register_blueprint("test-registry-dft", "Test Registry Dft", bp)
        registered_names.append(reg.canonical_name)

        assert isinstance(reg, BlueprintRegistry)
        assert reg.canonical_name == "test-registry-dft"
        assert reg.display_name == "Test Registry Dft"
        assert reg.blueprint is bp
        assert reg.is_exportable is True
        assert reg.always_apply is False
        assert reg.user_invokable is True
        assert reg.llm_invokable is True
        assert reg.conditional_sidecars == ()
        assert reg.affordances is None
        assert blueprint_registry["test-registry-dft"] is reg
        assert exportable_registry["test-registry-dft"] is reg

    def test_flags(_, corpus_testee1, registered_names):
        bp = PromptBlueprint.create_empty_blueprint(
            corpus_tree=corpus_testee1
        )

        reg = register_blueprint(
            "test-registry-flags",
            "Test Registry Flags",
            bp,
            always_apply=True,
            user_invokable=False,
            llm_invokable=False,
        )
        registered_names.append(reg.canonical_name)

        assert reg.is_exportable is True
        assert reg.always_apply is True
        assert reg.user_invokable is False
        assert reg.llm_invokable is False
        assert exportable_registry["test-registry-flags"] is reg

    def test_is_exportable_false_skips_exportable_registry(
        _, corpus_testee1, registered_names
    ):
        bp = PromptBlueprint.create_empty_blueprint(
            corpus_tree=corpus_testee1
        )

        reg = register_blueprint(
            "test-registry-internal",
            "Test Registry Internal",
            bp,
            is_exportable=False,
        )
        registered_names.append(reg.canonical_name)

        assert reg.is_exportable is False
        assert blueprint_registry["test-registry-internal"] is reg
        assert "test-registry-internal" not in exportable_registry

    def test_conditional_sidecars_and_affordances(
        _, corpus_testee1, registered_names
    ):
        bp = PromptBlueprint.create_empty_blueprint(
            corpus_tree=corpus_testee1
        )

        reg = register_blueprint(
            "test-registry-sidecars",
            "Test Registry Sidecars",
            bp,
            conditional_sidecars=("for Kaye",),
            affordances=(),
        )
        registered_names.append(reg.canonical_name)

        assert reg.conditional_sidecars == ("for Kaye",)
        assert reg.affordances == ()

    def test_duplicate_name(_, corpus_testee1, registered_names):
        bp = PromptBlueprint.create_empty_blueprint(
            corpus_tree=corpus_testee1
        )

        reg = register_blueprint("test-registry-dup", "Test Registry Dup", bp)
        registered_names.append(reg.canonical_name)

        with pytest.raises(ValueError) as exec_info:
            register_blueprint("test-registry-dup", "Another Name", bp)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "duplicate blueprint registry name: test-registry-dup"


class TestBlueprintRegistryContent:  ############################################

    def test_forwards_registry_defaults(_, corpus_testee1, monkeypatch):
        bp = PromptBlueprint.create_empty_blueprint(
            corpus_tree=corpus_testee1
        )
        captured = {}
        monkeypatch.setattr(
            bp,
            "generate_prompt",
            lambda **kwargs: captured.update(kwargs),
        )

        reg = BlueprintRegistry(
            canonical_name="test-content-dft",
            display_name="Test Content Dft",
            blueprint=bp,
            conditional_sidecars=("for Kaye",),
            affordances=(),
        )
        reg.content()

        assert captured["conditional_sidecars"] == ("for Kaye",)
        assert captured["affordances"] == ()

    def test_explicit_kwargs_merge_with_registry_defaults(
        _, corpus_testee1, monkeypatch
    ):
        bp = PromptBlueprint.create_empty_blueprint(
            corpus_tree=corpus_testee1
        )
        captured = {}
        monkeypatch.setattr(
            bp,
            "generate_prompt",
            lambda **kwargs: captured.update(kwargs),
        )

        reg = BlueprintRegistry(
            canonical_name="test-content-owr",
            display_name="Test Content Owr",
            blueprint=bp,
            conditional_sidecars=("for Kaye",),
            affordances=(),
        )
        reg.content(conditional_sidecars=("for Ria",), affordances=None)

        # explicit kwargs are unioned with the registry's own defaults
        # rather than replacing them, so a caller-supplied value (e.g.
        # surface-derived sidecars/affordances from the CLI) never
        # clobbers this entry's own registered defaults
        assert captured["conditional_sidecars"] == ("for Kaye", "for Ria")
        assert captured["affordances"] == ()
