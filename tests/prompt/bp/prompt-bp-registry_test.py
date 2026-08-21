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
from kaye_engine.prompt.blueprint.render_profile import RenderProfile


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
        assert reg.user_invokable is True
        assert reg.llm_invokable is True
        assert reg.render_profile == RenderProfile()
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
            user_invokable=False,
            llm_invokable=False,
        )
        registered_names.append(reg.canonical_name)

        assert reg.is_exportable is True
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

    def test_conditional_sidecars_and_variants(
        _, corpus_testee1, registered_names
    ):
        bp = PromptBlueprint.create_empty_blueprint(
            corpus_tree=corpus_testee1
        )

        reg = register_blueprint(
            "test-registry-sidecars",
            "Test Registry Sidecars",
            bp,
            render_profile=RenderProfile(
                conditional_sidecars=("for Kaye",), variants=()
            ),
        )
        registered_names.append(reg.canonical_name)

        assert reg.render_profile.conditional_sidecars == ("for Kaye",)
        assert reg.render_profile.variants == ()

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
            render_profile=RenderProfile(
                conditional_sidecars=("for Kaye",), variants=()
            ),
        )
        reg.content()

        assert captured["profile"].conditional_sidecars == ("for Kaye",)
        assert captured["profile"].variants == ()

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
            render_profile=RenderProfile(
                conditional_sidecars=("for Kaye",), variants=()
            ),
        )
        reg.content(
            profile=RenderProfile(
                conditional_sidecars=("for Ria",), variants=None
            )
        )

        # the explicit profile is unioned with the registry's own
        # defaults rather than replacing them, so a caller-supplied
        # value (e.g. surface-derived sidecars/variants from the
        # CLI) never clobbers this entry's own registered defaults
        assert captured["profile"].conditional_sidecars == (
            "for Kaye",
            "for Ria",
        )
        assert captured["profile"].variants == ()
