"""
image_prompt_export_test.py

Unit Tests (using pytest) for:

- register_image_prompt_exportable()
- image_prompt_exportable_registry
"""

import pytest

from kaye_engine.exportable import (
    image_prompt_exportable_registry,
    exportable_registry,
    register_image_prompt_exportable,
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
        if name in image_prompt_exportable_registry:
            image_prompt_exportable_registry.remove(name)


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


class TestRegisterImagePromptExportable:  ###################################

    def test_dft(_, empty_corpus, registered_names):
        reg = _dummy_blueprint_registry("test-image-prompt-dft", empty_corpus)
        registered_names.append(reg.canonical_name)
        register_exportable_entry(reg)

        opt = register_image_prompt_exportable("test-image-prompt-dft")

        assert opt == "test-image-prompt-dft"
        assert "test-image-prompt-dft" in image_prompt_exportable_registry

    def test_unknown_name(_):
        with pytest.raises(KeyError):
            register_image_prompt_exportable("test-image-prompt-no-such-name")

    def test_duplicate_name(_, empty_corpus, registered_names):
        reg = _dummy_blueprint_registry("test-image-prompt-dup", empty_corpus)
        registered_names.append(reg.canonical_name)
        register_exportable_entry(reg)
        register_image_prompt_exportable("test-image-prompt-dup")

        with pytest.raises(ValueError) as exec_info:
            register_image_prompt_exportable("test-image-prompt-dup")

        opt = exec_info.value.args[0]
        assert opt == (
            "duplicate image-prompt exportable registry name: "
            "test-image-prompt-dup"
        )
