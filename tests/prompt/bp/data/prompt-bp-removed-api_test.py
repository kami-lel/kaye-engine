"""
prompt-bp-removed-api_test.py

Unit Tests (using pytest) for:

the removed `PromptBlueprint` surface failing loudly, so a stale caller
cannot silently keep a discarded result
"""

import pytest

from kaye_engine.prompt.blueprint.data import Blueprint, create_blueprint


class TestRemovedMethods:

    @pytest.mark.parametrize(
        "name",
        [
            "checkmark",
            "uncheckmark",
            "merge",
            "prune",
            "render_prompt",
            "render_blueprint",
            "generate_prompt_without_dependencies",
            "is_checkmarked",
            "sidecars",
            "corpus",
        ],
    )
    def test_attribute_access_raises(_, name):
        with pytest.raises(AttributeError):
            getattr(create_blueprint(), name)

    def test_checkmark_statement_style_fails(_):
        bp = create_blueprint()

        with pytest.raises(AttributeError):
            bp.checkmark("Anything")

    def test_item_assignment_fails(_):
        with pytest.raises(TypeError):
            create_blueprint()[123] = True

    def test_or_operator_fails(_):
        with pytest.raises(TypeError):
            create_blueprint() | create_blueprint()

    def test_attribute_assignment_fails(_):
        # CPython raises TypeError for an unknown name on a frozen slots
        # dataclass, FrozenInstanceError (an AttributeError) for a field
        with pytest.raises((AttributeError, TypeError)):
            create_blueprint().sidecars = None


class TestRemovedNames:

    def test_prompt_blueprint_not_importable(_):
        with pytest.raises(ImportError):
            from kaye_engine.prompt import PromptBlueprint  # noqa: F401

    def test_default_corpus_tree_not_importable(_):
        with pytest.raises(ImportError):
            from kaye_engine import get_default_corpus_tree  # noqa: F401

    def test_hash_integer_node_argument_rejected(_):
        from kaye_engine.prompt.blueprint.edit import checkmark_nodes
        from kaye_engine.prompt.prompt_corpus_loader import (
            clear_corpus_tree,
            load_corpus_tree,
        )

        clear_corpus_tree()
        load_corpus_tree(["# A\n"])
        try:
            with pytest.raises(TypeError):
                checkmark_nodes(Blueprint(), hash("A"))
        finally:
            clear_corpus_tree()


class TestRenamedPreviewNames:

    @pytest.mark.parametrize(
        "name",
        [
            "render_blueprint",
            "render_blueprint_without_dependencies",
            "render_blueprint_tree",
        ],
    )
    def test_old_preview_name_not_importable(_, name):
        with pytest.raises(ImportError):
            exec("from kaye_engine.prompt.blueprint import " + name)


class TestRenamedShowNames:

    @pytest.mark.parametrize(
        "name",
        [
            "render_description",
            "render_when_to_use",
            "render_description_and_when_to_use",
            "extract_globs",
        ],
    )
    def test_old_show_name_not_importable(_, name):
        with pytest.raises(ImportError):
            exec("from kaye_engine.prompt.blueprint import " + name)
