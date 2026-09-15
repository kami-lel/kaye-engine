"""
comfy_ui_export_parser_test.py

Unit Tests (using pytest) for:

_comfy_ui_export_main, register_comfy_ui_export_parser
"""

from argparse import ArgumentParser
from unittest.mock import patch

import pytest

from kaye_engine.cli import comfy_ui_export_parser
from kaye_engine.exportable import Exportable
from kaye_engine.prompt.blueprint import PromptBlueprint
from kaye_engine.prompt.blueprint.registry import BlueprintRegistry
from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode


# auxiliaries  ##################################################################
class _FakeExportable(Exportable):

    def content(self, **_render_kwargs):
        return "fake exportable content for " + self.canonical_name

    def merge(self, other):
        raise NotImplementedError("_FakeExportable does not support merge()")


_AVOID_CONTENT_BY_NAME = {"some-exportable": "don't do this"}


def _build_comfy_ui_export_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    comfy_ui_export_parser.register_comfy_ui_export_parser(subparser)
    return root_parser


@pytest.fixture(autouse=True)
def _no_corpus_setup_guard():
    with patch.object(
        comfy_ui_export_parser, "check_corpus_setup_for_cli", lambda: None
    ):
        yield


@pytest.fixture
def _fake_registry():
    registry = {
        "some-exportable": _FakeExportable(
            canonical_name="some-exportable", display_name="Some Exportable"
        ),
        "other-exportable": _FakeExportable(
            canonical_name="other-exportable",
            display_name="Other Exportable",
        ),
    }
    with patch.object(
        comfy_ui_export_parser, "get_exportable", registry.__getitem__
    ), patch.object(
        comfy_ui_export_parser,
        "comfy_ui_exportable_registry",
        list(registry),
    ), patch.object(
        comfy_ui_export_parser,
        "_avoid_content",
        lambda exportable: _AVOID_CONTENT_BY_NAME.get(
            exportable.canonical_name, ""
        ),
    ):
        yield registry


# pytest  ######################################################################
class TestAvoidContent:

    def test_blueprint_with_avoid_content_renders_negative_prompt(_):
        root = PromptCorpusNode("○", None, [])
        main = PromptCorpusNode("Main", root, ["Main content."])
        PromptCorpusNode("{avoid}", main, ["Do not do this."])
        blueprint = PromptBlueprint.create_full_blueprint(corpus_tree=root)
        reg = BlueprintRegistry(
            canonical_name="test-avoid-with-content",
            display_name="Test",
            blueprint=blueprint,
        )

        opt = comfy_ui_export_parser._avoid_content(reg)

        assert opt == "Main:\nDo not do this."

    def test_blueprint_without_avoid_content_returns_empty(_):
        root = PromptCorpusNode("○", None, [])
        PromptCorpusNode("Main", root, ["Main content."])
        blueprint = PromptBlueprint.create_full_blueprint(corpus_tree=root)
        reg = BlueprintRegistry(
            canonical_name="test-avoid-without-content",
            display_name="Test",
            blueprint=blueprint,
        )

        opt = comfy_ui_export_parser._avoid_content(reg)

        assert opt == ""

    def test_exportable_without_negative_content_returns_empty(_):
        exportable = _FakeExportable(
            canonical_name="test-avoid-no-blueprint", display_name="Test"
        )

        opt = comfy_ui_export_parser._avoid_content(exportable)

        assert opt == ""


class TestRegisterComfyUiExportParser:

    def test_registers_comfy_ui_export_subcommand(self):
        parser = _build_comfy_ui_export_parser()
        args = parser.parse_args(["comfy-ui-export", "some-dir"])

        assert args.func is comfy_ui_export_parser._comfy_ui_export_main

    def test_registers_y_alias(self):
        parser = _build_comfy_ui_export_parser()
        args = parser.parse_args(["y", "some-dir"])

        assert args.func is comfy_ui_export_parser._comfy_ui_export_main
        assert args.folder == "some-dir"


class TestComfyUiExportMain:

    def test_writes_one_md_per_registered_name(
        self, _fake_registry, tmp_path
    ):
        folder = tmp_path / "out"
        parser = _build_comfy_ui_export_parser()
        args = parser.parse_args(["comfy-ui-export", str(folder)])
        args.func(args)

        assert (folder / "some-exportable.md").read_text(
            encoding="utf-8"
        ) == "fake exportable content for some-exportable"
        assert (folder / "other-exportable.md").read_text(
            encoding="utf-8"
        ) == "fake exportable content for other-exportable"

    def test_writes_avoid_md_only_when_content_present(
        self, _fake_registry, tmp_path
    ):
        folder = tmp_path / "out"
        parser = _build_comfy_ui_export_parser()
        args = parser.parse_args(["comfy-ui-export", str(folder)])
        args.func(args)

        assert (folder / "some-exportable-AVOID.md").read_text(
            encoding="utf-8"
        ) == "don't do this"
        assert not (folder / "other-exportable-AVOID.md").exists()

    def test_y_alias_writes_same_output(self, _fake_registry, tmp_path):
        folder = tmp_path / "out"
        parser = _build_comfy_ui_export_parser()
        args = parser.parse_args(["y", str(folder)])
        args.func(args)

        assert (folder / "some-exportable.md").is_file()
        assert (folder / "other-exportable.md").is_file()

    def test_creates_folder_when_missing(self, _fake_registry, tmp_path):
        folder = tmp_path / "does" / "not" / "exist"
        parser = _build_comfy_ui_export_parser()
        args = parser.parse_args(["comfy-ui-export", str(folder)])
        args.func(args)

        assert folder.is_dir()

    def test_only_writes_exportables_in_the_subset(
        self, _fake_registry, tmp_path
    ):
        folder = tmp_path / "out"
        with patch.object(
            comfy_ui_export_parser,
            "comfy_ui_exportable_registry",
            ["some-exportable"],
        ):
            parser = _build_comfy_ui_export_parser()
            args = parser.parse_args(["comfy-ui-export", str(folder)])
            args.func(args)

        assert (folder / "some-exportable.md").is_file()
        assert not (folder / "other-exportable.md").exists()
