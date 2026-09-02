"""
exportable_test.py

Unit Tests (using pytest) for:

- Exportable
- register_exportable_entry()
- get_exportable()
- content() on BlueprintRegistry and ExportableAbbr
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
from kaye_engine.prompt.blueprint import BlueprintRegistry, PromptBlueprint
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode


@pytest.fixture
def registered_names():
    names = []
    yield names
    for name in names:
        exportable_registry.pop(name, None)


@pytest.fixture
def empty_corpus():
    return PromptCorpusNode("○", None, [])


def _dummy_blueprint_registry(canonical_name, empty_corpus, **kwargs):
    return BlueprintRegistry(
        canonical_name=canonical_name,
        display_name="Test " + canonical_name,
        blueprint=PromptBlueprint.create_empty_blueprint(
            corpus_tree=empty_corpus
        ),
        **kwargs,
    )


class TestExportableIsAbstract:  ################################################

    def test_cannot_instantiate_directly(_):
        with pytest.raises(TypeError):
            Exportable(canonical_name="x", display_name="X")


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
        ) == reg.blueprint.generate_prompt_without_dependencies(sparseness=0)

    def test_blueprint_registry_content_forwards_render_kwargs(
        _, empty_corpus
    ):
        reg = _dummy_blueprint_registry("test-exp-content-kw", empty_corpus)

        assert reg.content(
            profile=RenderProfile(sparseness=-1)
        ) == reg.blueprint.generate_prompt_without_dependencies(sparseness=-1)

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
