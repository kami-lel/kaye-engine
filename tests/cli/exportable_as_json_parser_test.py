"""
exportable_as_json_parser_test.py

Unit Tests (using pytest) for:

_exportable_as_json_main, register_exportable_as_json_parser
"""

import json
from argparse import ArgumentParser
from unittest.mock import patch

import pytest

from kaye_engine.cli import exportable_as_json_parser
from kaye_engine.exportable import Exportable


# auxiliaries  ##################################################################
class _FakeExportable(Exportable):

    def content(self, **_render_kwargs):
        return "fake exportable content for " + self.canonical_name

    def merge(self, other):
        raise NotImplementedError("_FakeExportable does not support merge()")


def _build_exportable_as_json_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    exportable_as_json_parser.register_exportable_as_json_parser(subparser)
    return root_parser


@pytest.fixture(autouse=True)
def _no_corpus_setup_guard():
    with patch.object(
        exportable_as_json_parser, "check_corpus_setup_for_cli", lambda: None
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
        exportable_as_json_parser, "exportable_registry", registry
    ), patch.object(
        exportable_as_json_parser, "get_exportable", registry.__getitem__
    ):
        yield registry


# pytest  ######################################################################
class TestRegisterExportableAsJsonParser:

    def test_registers_exportable_as_json_subcommand(self):
        parser = _build_exportable_as_json_parser()
        args = parser.parse_args(["exportable-as-json"])

        assert args.func is (
            exportable_as_json_parser._exportable_as_json_main
        )

    def test_registers_j_alias(self):
        parser = _build_exportable_as_json_parser()
        args = parser.parse_args(["j"])

        assert args.func is (
            exportable_as_json_parser._exportable_as_json_main
        )


class TestExportableAsJsonMainFullExport:

    def test_writes_every_entry_keyed_by_canonical_name(
        self, _fake_registry, tmp_path
    ):
        output_file = tmp_path / "out.json"
        parser = _build_exportable_as_json_parser()
        args = parser.parse_args(
            ["exportable-as-json", "--output-file", str(output_file)]
        )
        args.func(args)

        written = json.loads(output_file.read_text(encoding="utf-8"))
        assert written == {
            "some-exportable": "fake exportable content for "
            "some-exportable",
            "other-exportable": "fake exportable content for "
            "other-exportable",
        }

    def test_j_alias_writes_same_output(self, _fake_registry, tmp_path):
        output_file = tmp_path / "out.json"
        parser = _build_exportable_as_json_parser()
        args = parser.parse_args(["j", "-f", str(output_file)])
        args.func(args)

        written = json.loads(output_file.read_text(encoding="utf-8"))
        assert set(written) == {"some-exportable", "other-exportable"}

    def test_default_output_file_when_omitted(
        self, _fake_registry, tmp_path, monkeypatch
    ):
        monkeypatch.chdir(tmp_path)
        parser = _build_exportable_as_json_parser()
        args = parser.parse_args(["exportable-as-json"])
        args.func(args)

        default_output = tmp_path / "exportable-as-json.json"
        assert default_output.is_file()
        written = json.loads(default_output.read_text(encoding="utf-8"))
        assert set(written) == {"some-exportable", "other-exportable"}

    def test_output_file_flag_writes_to_given_path(
        self, _fake_registry, tmp_path
    ):
        output_file = tmp_path / "custom.json"
        parser = _build_exportable_as_json_parser()
        args = parser.parse_args(
            ["exportable-as-json", "--output-file", str(output_file)]
        )
        args.func(args)

        assert output_file.is_file()


class TestExportableAsJsonMainComfyUiSubset:

    def test_flag_exports_exactly_the_subset(
        self, _fake_registry, tmp_path
    ):
        output_file = tmp_path / "comfy.json"
        with patch.object(
            exportable_as_json_parser,
            "comfy_ui_exportable_registry",
            ["some-exportable"],
        ):
            parser = _build_exportable_as_json_parser()
            args = parser.parse_args(
                [
                    "exportable-as-json",
                    "--comfy-ui",
                    "--output-file",
                    str(output_file),
                ]
            )
            args.func(args)

        written = json.loads(output_file.read_text(encoding="utf-8"))
        assert written == {
            "some-exportable": {
                "positive": "fake exportable content for "
                "some-exportable",
                "negative": "",
            },
        }

    def test_y_alias_exports_exactly_the_subset(
        self, _fake_registry, tmp_path
    ):
        output_file = tmp_path / "comfy.json"
        with patch.object(
            exportable_as_json_parser,
            "comfy_ui_exportable_registry",
            ["other-exportable"],
        ):
            parser = _build_exportable_as_json_parser()
            args = parser.parse_args(
                ["exportable-as-json", "-y", "-f", str(output_file)]
            )
            args.func(args)

        written = json.loads(output_file.read_text(encoding="utf-8"))
        assert set(written) == {"other-exportable"}
        assert written["other-exportable"]["positive"] == (
            "fake exportable content for other-exportable"
        )
        assert written["other-exportable"]["negative"] == ""

    def test_flag_absent_still_exports_everything(
        self, _fake_registry, tmp_path
    ):
        output_file = tmp_path / "all.json"
        with patch.object(
            exportable_as_json_parser,
            "comfy_ui_exportable_registry",
            ["some-exportable"],
        ):
            parser = _build_exportable_as_json_parser()
            args = parser.parse_args(
                ["exportable-as-json", "-f", str(output_file)]
            )
            args.func(args)

        written = json.loads(output_file.read_text(encoding="utf-8"))
        assert set(written) == {"some-exportable", "other-exportable"}
