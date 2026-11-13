"""
exportable_parser_test.py

Unit Tests (using pytest) for:

_exportable_main, register_exportable_parser
"""

import io
import logging
from argparse import ArgumentParser
from unittest.mock import patch

import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.cli import exportable_parser
from kaye_engine.exportable import Exportable


# auxiliaries  ##################################################################
class _Tty(io.StringIO):
    def isatty(self):
        return True


class _FakeExportable(Exportable):

    def content(self, **_render_kwargs):
        return "fake exportable content for " + self.canonical_name

    def merge(self, other):
        raise NotImplementedError("_FakeExportable does not support merge()")


def _build_exportable_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    exportable_parser.register_exportable_parser(subparser)
    return root_parser


@pytest.fixture(autouse=True)
def _no_corpus_setup_guard():
    with patch.object(
        exportable_parser, "check_corpus_setup_for_cli", lambda: None
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
    with patch.object(exportable_parser, "exportable_registry", registry):
        yield registry


# pytest  ######################################################################
class TestRegisterExportableParser:

    def test_registers_exportable_subcommand(self):
        parser = _build_exportable_parser()
        args = parser.parse_args(["exportable", "some-exportable"])

        assert args.EXPORTABLE == "some-exportable"
        assert args.func is exportable_parser._exportable_main

    def test_registers_x_alias(self):
        parser = _build_exportable_parser()
        args = parser.parse_args(["x", "some-exportable"])

        assert args.EXPORTABLE == "some-exportable"

    def test_bare_command_defaults_to_ls(self):
        parser = _build_exportable_parser()

        assert parser.parse_args(["x"]).EXPORTABLE == "ls"


class TestExportableMainLs:

    def test_lists_registered_exportables_sorted(
        self, _fake_registry, capsys
    ):
        parser = _build_exportable_parser()
        args = parser.parse_args(["exportable", "ls"])
        args.func(args)

        out = capsys.readouterr().out
        assert out.splitlines() == ["other-exportable", "some-exportable"]

    def test_tty_has_banner_and_colored_names(
        self, _fake_registry, monkeypatch
    ):
        monkeypatch.delenv("NO_COLOR", raising=False)
        tty = _Tty()
        monkeypatch.setattr("sys.stdout", tty)
        parser = _build_exportable_parser()
        args = parser.parse_args(["exportable", "ls"])
        args.func(args)

        out = tty.getvalue()
        assert "  exportables (2)  " in out
        assert "\033[96mother-exportable\033[0m" in out

    def test_lists_nothing_when_registry_empty(self, capsys):
        with patch.object(exportable_parser, "exportable_registry", {}):
            parser = _build_exportable_parser()
            args = parser.parse_args(["exportable", "ls"])
            args.func(args)

        out = capsys.readouterr().out
        assert out == ""


class TestExportableMainPrintsContent:

    def test_prints_content_of_known_exportable(
        self, _fake_registry, capsys
    ):
        parser = _build_exportable_parser()
        args = parser.parse_args(["exportable", "some-exportable"])
        args.func(args)

        out = capsys.readouterr().out
        assert "fake exportable content for some-exportable" in out


class TestExportableMainUnknownExportable:

    def test_exits_on_unknown_exportable(self, _fake_registry):
        parser = _build_exportable_parser()
        args = parser.parse_args(["exportable", "does-not-exist"])

        with pytest.raises(SystemExit):
            args.func(args)

    def test_logs_error_on_unknown_exportable(
        self, _fake_registry, caplog
    ):
        parser = _build_exportable_parser()
        args = parser.parse_args(["exportable", "does-not-exist"])

        with caplog.at_level(logging.ERROR, logger=LOGGER_NAME):
            with pytest.raises(SystemExit):
                args.func(args)

        assert any(
            rec.levelno == logging.ERROR for rec in caplog.records
        )
        assert any(
            "unknown exportable: does-not-exist" in rec.message
            for rec in caplog.records
        )

    def test_names_the_closest_when_near(self, _fake_registry, caplog):
        parser = _build_exportable_parser()
        args = parser.parse_args(["exportable", "some-exportble"])

        with caplog.at_level(logging.ERROR, logger=LOGGER_NAME):
            with pytest.raises(SystemExit):
                args.func(args)

        assert "did you mean: some-exportable" in caplog.text


class TestModeGuard:

    @pytest.mark.parametrize(
        "flag",
        [["-s", "0"], ["-u", "claude"], ["--comment"], ["--reverse-order"]],
    )
    def test_list_mode_rejects_render_flags(self, _fake_registry, flag):
        args = _build_exportable_parser().parse_args(["x", *flag])

        with pytest.raises(SystemExit) as info:
            exportable_parser._exportable_main(args)

        assert info.value.code == 1

    @pytest.mark.parametrize("flag", [["-r", "x"], ["-N"], ["-f", "json"]])
    def test_entry_mode_rejects_list_flags(self, _fake_registry, flag):
        args = _build_exportable_parser().parse_args(
            ["x", "some-exportable", *flag]
        )

        with pytest.raises(SystemExit) as info:
            exportable_parser._exportable_main(args)

        assert info.value.code == 1

    def test_list_mode_takes_list_flags(self, _fake_registry, capsys):
        args = _build_exportable_parser().parse_args(["x", "-r", "^other"])
        exportable_parser._exportable_main(args)

        assert capsys.readouterr().out == "other-exportable\n"
