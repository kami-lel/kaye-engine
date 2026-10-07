"""
exportable_test.py

Unit Tests (using pytest) for:

- Exportable
- register_exportable_entry()
- get_exportable()
- content() / negative_content() on BlueprintRegistry and ExportableAbbr
"""

import pytest

from kaye_engine.abbr_collection import AbbrEntry, AbbrMeaning
from kaye_engine.cli.exportable_abbr import ExportableAbbr
from kaye_engine.exportable import (
    Exportable,
    exportable_registry,
    get_exportable,
    register_exportable_entry,
)
from kaye_engine.prompt.blueprint import BlueprintRegistry
from kaye_engine.prompt.blueprint.data import create_blueprint
from kaye_engine.prompt.blueprint.render import render_prompt_without_dependencies
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
        exportable_registry.pop(name, None)


@pytest.fixture
def empty_corpus():
    clear_corpus_tree()
    root = load_corpus_tree([])
    yield root
    clear_corpus_tree()


def _dummy_blueprint_registry(canonical_name, empty_corpus, **kwargs):
    return BlueprintRegistry(
        canonical_name=canonical_name,
        display_name="Test " + canonical_name,
        blueprint=create_blueprint(),
        **kwargs,
    )


class TestExportableIsAbstract:  ################################################

    def test_cannot_instantiate_directly(_):
        with pytest.raises(TypeError):
            Exportable(canonical_name="x", display_name="X")


class TestAlwaysApply:  #########################################################

    def test_dft_false(_, empty_corpus):
        reg = _dummy_blueprint_registry("test-exp-aa-dft", empty_corpus)

        assert reg.always_apply is False

    def test_set_true(_, empty_corpus):
        reg = _dummy_blueprint_registry(
            "test-exp-aa-set", empty_corpus, always_apply=True
        )

        assert reg.always_apply is True

    def test_abbr_group_dft_false(_):
        group = ExportableAbbr(
            canonical_name="test-exp-aa-abbr", display_name="Test Abbr"
        )

        assert group.always_apply is False


class TestRegisterExportableEntry:  #############################################

    def test_dft(_, empty_corpus, registered_names):
        reg = _dummy_blueprint_registry("test-exp-dft", empty_corpus)
        registered_names.append(reg.canonical_name)

        opt = register_exportable_entry(reg)

        assert opt is reg
        assert exportable_registry["test-exp-dft"] is reg

    def test_duplicate_name(_, empty_corpus, registered_names):
        reg = _dummy_blueprint_registry("test-exp-dup", empty_corpus)
        registered_names.append(reg.canonical_name)
        register_exportable_entry(reg)

        with pytest.raises(ValueError) as exec_info:
            register_exportable_entry(
                _dummy_blueprint_registry("test-exp-dup", empty_corpus)
            )

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "duplicate exportable registry name: test-exp-dup"


class TestGetExportable:  #######################################################

    def test_known_name(_, empty_corpus, registered_names):
        reg = _dummy_blueprint_registry("test-exp-get", empty_corpus)
        registered_names.append(reg.canonical_name)
        register_exportable_entry(reg)

        assert get_exportable("test-exp-get") is reg

    def test_unknown_name(_):
        with pytest.raises(KeyError):
            get_exportable("test-exp-no-such-name")


class TestContent:  #############################################################

    def test_blueprint_registry_content(_, empty_corpus):
        reg = _dummy_blueprint_registry("test-exp-content", empty_corpus)

        assert reg.content(
            profile=RenderProfile(sparseness=0)
        ) == render_prompt_without_dependencies(
            reg.blueprint, profile=RenderProfile(sparseness=0)
        )

    def test_blueprint_registry_content_forwards_render_kwargs(
        _, empty_corpus
    ):
        reg = _dummy_blueprint_registry("test-exp-content-kw", empty_corpus)

        assert reg.content(
            profile=RenderProfile(sparseness=-1)
        ) == render_prompt_without_dependencies(
            reg.blueprint, profile=RenderProfile(sparseness=-1)
        )

    def test_blueprint_registry_content_comment_names_entry(_, empty_corpus):
        reg = _dummy_blueprint_registry("test-exp-name", empty_corpus)

        opt = reg.content(profile=RenderProfile(show_comment=True))

        assert "blueprint: Test test-exp-name\n" in opt

    def test_blueprint_registry_content_keeps_explicit_display_name(
        _, empty_corpus
    ):
        reg = _dummy_blueprint_registry("test-exp-keep", empty_corpus)

        opt = reg.content(
            profile=RenderProfile(show_comment=True, display_name="Mine")
        )

        assert "blueprint: Mine\n" in opt
        assert "Test test-exp-keep" not in opt

    def test_exportable_abbr_content(_):
        entry = AbbrEntry(
            AbbrMeaning("for example", remark=None),
            "e.g.",
            {"priority": 5, "tags": [], "wrap": "word"},
        )
        group = ExportableAbbr(
            [entry], canonical_name="test-exp-abbr", display_name="Test"
        )

        assert group.content() == group.as_md_list()
        assert group.content() == entry.as_md_list_entry()
        assert group.content(sparseness=0, show_comment=True) == (
            group.as_md_list()
        )


class TestNegativeContent:  #####################################################

    @pytest.fixture(autouse=True)
    def _avoid_corpus(_):
        clear_corpus_tree()
        load_corpus_tree(["# Main\nMain content.\n## {avoid}\nDo not do this.\n"])
        yield
        clear_corpus_tree()

    def test_blueprint_registry_negative_content(_):
        blueprint = create_blueprint(is_full=True)
        reg = BlueprintRegistry(
            canonical_name="test-exp-negative-content",
            display_name="Test Negative Content",
            blueprint=blueprint,
        )

        assert (
            reg.content(profile=RenderProfile(mode=RenderMode.NEGATIVE))
            == "# Main\nDo not do this."
        )

    def test_blueprint_registry_negative_content_forwards_profile(_):
        blueprint = create_blueprint(is_full=True)
        reg = BlueprintRegistry(
            canonical_name="test-exp-negative-content-kw",
            display_name="Test Negative Content Kw",
            blueprint=blueprint,
        )
        profile = RenderProfile(sparseness=0, mode=RenderMode.NEGATIVE)

        assert reg.content(
            profile=profile
        ) == render_prompt_without_dependencies(
            reg.blueprint, profile=profile
        )


class TestExportableAbbrMerge:  #################################################

    def test_merge_raises_not_implemented(_):
        entry = AbbrEntry(
            AbbrMeaning("for example", remark=None),
            "e.g.",
            {"priority": 5, "tags": [], "wrap": "word"},
        )
        group_a = ExportableAbbr(
            [entry], canonical_name="abbr-merge-a", display_name="A"
        )
        group_b = ExportableAbbr(
            [entry], canonical_name="abbr-merge-b", display_name="B"
        )

        with pytest.raises(NotImplementedError):
            group_a.merge(group_b)
