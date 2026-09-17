"""
comfy_ui_export_test.py

Unit Tests (using pytest) for:

- register_comfy_ui_exportable()
- comfy_ui_exportable_registry
"""

import pytest

from kaye_engine.exportable import (
    comfy_ui_exportable_registry,
    exportable_registry,
    register_comfy_ui_exportable,
    register_exportable_entry,
)
from kaye_engine.prompt.blueprint import BlueprintRegistry, PromptBlueprint
from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode


@pytest.fixture
def registered_names():
    names = []
    yield names
    for name in names:
        exportable_registry.pop(name, None)
        if name in comfy_ui_exportable_registry:
            comfy_ui_exportable_registry.remove(name)


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


class TestRegisterComfyUiExportable:  ############################################

    def test_dft(_, empty_corpus, registered_names):
        reg = _dummy_blueprint_registry("test-comfy-dft", empty_corpus)
        registered_names.append(reg.canonical_name)
        register_exportable_entry(reg)

        opt = register_comfy_ui_exportable("test-comfy-dft")

        assert opt == "test-comfy-dft"
        assert "test-comfy-dft" in comfy_ui_exportable_registry

    def test_unknown_name(_):
        with pytest.raises(KeyError):
            register_comfy_ui_exportable("test-comfy-no-such-name")

    def test_duplicate_name(_, empty_corpus, registered_names):
        reg = _dummy_blueprint_registry("test-comfy-dup", empty_corpus)
        registered_names.append(reg.canonical_name)
        register_exportable_entry(reg)
        register_comfy_ui_exportable("test-comfy-dup")

        with pytest.raises(ValueError) as exec_info:
            register_comfy_ui_exportable("test-comfy-dup")

        opt = exec_info.value.args[0]
        assert opt == (
            "duplicate comfy-ui exportable registry name: test-comfy-dup"
        )
