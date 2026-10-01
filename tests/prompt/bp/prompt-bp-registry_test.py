"""
prompt-bp-registry_test.py

Unit Tests (using pytest) for:

- register_blueprint()
- BlueprintRegistry
"""

import pytest

from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint.data import (
    Blueprint,
    BlueprintMeta,
    create_blueprint,
)
from kaye_engine.prompt.blueprint.edit import replace_meta
from kaye_engine.prompt.blueprint.registry import (
    BlueprintRegistry,
    register_blueprint,
    blueprint_registry,
)
from kaye_engine.prompt.blueprint.render_mode import RenderMode
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.prompt_corpus_loader import (
    clear_corpus_tree,
    load_corpus_tree,
)


@pytest.fixture
def registered_names():
    names = []
    yield names
    for name in names:
        blueprint_registry.pop(name, None)
        exportable_registry.pop(name, None)


class TestDisplayName:  ########################################################

    def test_meta_name_is_the_entry_name(_, registered_names):
        bp = Blueprint(meta=BlueprintMeta(display_name="From Meta"))

        reg = register_blueprint("test-registry-meta-name", bp)
        registered_names.append(reg.canonical_name)

        assert reg.display_name == "From Meta"

    def test_meta_name_beats_explicit_argument(_, registered_names):
        bp = Blueprint(meta=BlueprintMeta(display_name="From Meta"))

        reg = register_blueprint(
            "test-registry-meta-wins", bp, display_name="Explicit"
        )
        registered_names.append(reg.canonical_name)

        assert reg.display_name == "From Meta"

    def test_explicit_argument_is_the_fallback(_, registered_names):
        reg = register_blueprint(
            "test-registry-fallback",
            create_blueprint(),
            display_name="Explicit",
        )
        registered_names.append(reg.canonical_name)

        assert reg.display_name == "Explicit"

    def test_empty_everywhere_is_empty(_, registered_names):
        reg = register_blueprint("test-registry-unnamed", create_blueprint())
        registered_names.append(reg.canonical_name)

        assert reg.display_name == ""

    def test_reassigned_blueprint_is_read_live(_, registered_names):
        reg = register_blueprint("test-registry-live", create_blueprint())
        registered_names.append(reg.canonical_name)

        reg.blueprint = replace_meta(reg.blueprint, display_name="Later")

        assert reg.display_name == "Later"


class TestRegisterBlueprint:  ###################################################

    def test_dft(_, registered_names):
        bp = create_blueprint()

        reg = register_blueprint(
            "test-registry-dft",
            bp,
            display_name="Test Registry Dft",
        )
        registered_names.append(reg.canonical_name)

        assert isinstance(reg, BlueprintRegistry)
        assert reg.canonical_name == "test-registry-dft"
        assert reg.display_name == "Test Registry Dft"
        assert reg.blueprint is bp
        assert reg.is_exportable is True
        assert reg.is_user_invokable is True
        assert reg.llm_invokable is True
        assert reg.always_apply is False
        assert reg.render_profile == RenderProfile()
        assert blueprint_registry["test-registry-dft"] is reg
        assert exportable_registry["test-registry-dft"] is reg

    def test_flags(_, registered_names):
        bp = create_blueprint()

        reg = register_blueprint(
            "test-registry-flags",
            bp,
            display_name="Test Registry Flags",
            is_user_invokable=False,
            llm_invokable=False,
            always_apply=True,
        )
        registered_names.append(reg.canonical_name)

        assert reg.is_exportable is True
        assert reg.is_user_invokable is False
        assert reg.llm_invokable is False
        assert reg.always_apply is True
        assert exportable_registry["test-registry-flags"] is reg

    def test_is_exportable_false_skips_exportable_registry(
        _, registered_names
    ):
        bp = create_blueprint()

        reg = register_blueprint(
            "test-registry-internal",
            bp,
            display_name="Test Registry Internal",
            is_exportable=False,
        )
        registered_names.append(reg.canonical_name)

        assert reg.is_exportable is False
        assert blueprint_registry["test-registry-internal"] is reg
        assert "test-registry-internal" not in exportable_registry

    def test_conditional_sidecars_and_variants(
        _, registered_names
    ):
        bp = create_blueprint()

        reg = register_blueprint(
            "test-registry-sidecars",
            bp,
            display_name="Test Registry Sidecars",
            render_profile=RenderProfile(
                conditional_sidecars=("for Kaye",), variants=()
            ),
        )
        registered_names.append(reg.canonical_name)

        assert reg.render_profile.conditional_sidecars == ("for Kaye",)
        assert reg.render_profile.variants == ()

    def test_duplicate_name(_, registered_names):
        bp = create_blueprint()

        reg = register_blueprint(
            "test-registry-dup",
            bp,
            display_name="Test Registry Dup",
        )
        registered_names.append(reg.canonical_name)

        with pytest.raises(ValueError) as exec_info:
            register_blueprint(
                "test-registry-dup",
                bp,
                display_name="Another Name",
            )

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "duplicate blueprint registry name: test-registry-dup"


class TestBlueprintRegistryContent:  ############################################

    def test_forwards_registry_defaults(_, monkeypatch):
        bp = create_blueprint()
        captured = {}
        monkeypatch.setattr(
            "kaye_engine.prompt.blueprint.registry.render_prompt",
            lambda _bp, **kwargs: captured.update(kwargs),
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
        _, monkeypatch
    ):
        bp = create_blueprint()
        captured = {}
        monkeypatch.setattr(
            "kaye_engine.prompt.blueprint.registry.render_prompt",
            lambda _bp, **kwargs: captured.update(kwargs),
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


class TestRegisterValidation:  ##################################################

    def test_unknown_dependency_name_fails_at_registration(
        _, registered_names
    ):
        bp = create_blueprint(dependencies=["no-such-blueprint"])

        with pytest.raises(ValueError, match="no-such-blueprint"):
            register_blueprint(
                "test-registry-baddep",
                bp,
                display_name="Bad Dep",
            )

        assert "test-registry-baddep" not in blueprint_registry

    def test_unknown_dependency_inside_nested_value_fails(_):
        inner = Blueprint(dependencies=("no-such-blueprint",))
        bp = Blueprint(dependencies=(inner,))

        with pytest.raises(ValueError, match="no-such-blueprint"):
            register_blueprint(
                "test-registry-nested",
                bp,
                display_name="Nested",
            )

    def test_registered_dependency_is_accepted(_, registered_names):
        dep = register_blueprint(
            "test-registry-dep",
            create_blueprint(),
            display_name="Dep",
        )
        registered_names.append(dep.canonical_name)

        reg = register_blueprint(
            "test-registry-dependent",
            create_blueprint(dependencies=["test-registry-dep"]),
            display_name="Dependent",
        )
        registered_names.append(reg.canonical_name)

        assert reg.blueprint.dependencies == ("test-registry-dep",)

    def test_unknown_path_fails_while_corpus_loaded(_):
        clear_corpus_tree()
        load_corpus_tree(["# A\n"])
        bp = Blueprint(nodes=frozenset({("A", "Nope")}))

        with pytest.raises(ValueError, match="Nope"):
            register_blueprint(
                "test-registry-badpath",
                bp,
                display_name="Bad Path",
            )

        assert "test-registry-badpath" not in blueprint_registry

    def test_known_path_is_accepted(_, registered_names):
        clear_corpus_tree()
        load_corpus_tree(["# A\n"])

        reg = register_blueprint(
            "test-registry-goodpath",
            Blueprint(nodes=frozenset({("A",)})),
            display_name="Good Path",
        )
        registered_names.append(reg.canonical_name)

        assert reg.blueprint.nodes == {("A",)}

    def test_paths_unchecked_without_corpus(_, registered_names):
        clear_corpus_tree()

        reg = register_blueprint(
            "test-registry-nocorpus",
            Blueprint(nodes=frozenset({("Anything",)})),
            display_name="No Corpus",
        )
        registered_names.append(reg.canonical_name)

        assert reg.canonical_name in blueprint_registry


class TestResolveProfile:  ######################################################

    def test_entry_profile_is_the_base(_, registered_names):
        reg = register_blueprint(
            "test-registry-resolve",
            create_blueprint(),
            display_name="Resolve",
            render_profile=RenderProfile(mode=RenderMode.REVERSE_ORDER),
        )
        registered_names.append(reg.canonical_name)

        assert reg.resolve_profile().mode == RenderMode.REVERSE_ORDER

    def test_names_the_comment_after_the_entry(_, registered_names):
        reg = register_blueprint(
            "test-registry-resolve-name",
            create_blueprint(),
            display_name="Entry Name",
        )
        registered_names.append(reg.canonical_name)

        assert reg.resolve_profile().display_name == "Entry Name"

    def test_caller_chosen_name_wins(_, registered_names):
        reg = register_blueprint(
            "test-registry-resolve-own",
            create_blueprint(),
            display_name="Entry Name",
        )
        registered_names.append(reg.canonical_name)

        out = reg.resolve_profile(RenderProfile(display_name="Chosen"))

        assert out.display_name == "Chosen"
