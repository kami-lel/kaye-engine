"""
exportable_parser_test.py

Unit Tests (using pytest) for:

_export_main, register_export_parser
"""

import logging
from argparse import ArgumentParser
from unittest.mock import patch

import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.cli import exportable_parser
from kaye_engine.exportable import Exportable


# auxiliaries  ##################################################################
class _FakeExportable(Exportable):

    def content(self):
        return "fake exportable content for " + self.canonical_name


def _build_export_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    exportable_parser.register_export_parser(subparser)
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
class TestRegisterExportParser:

    def test_registers_export_subcommand(self):
        parser = _build_export_parser()
        args = parser.parse_args(["export", "some-exportable"])

        assert args.EXPORTABLE == "some-exportable"
        assert args.func is exportable_parser._export_main

    def test_registers_x_alias(self):
        parser = _build_export_parser()
        args = parser.parse_args(["x", "some-exportable"])

        assert args.EXPORTABLE == "some-exportable"


class TestExportMainLs:

    def test_lists_registered_exportables_sorted(
        self, _fake_registry, capsys
    ):
        parser = _build_export_parser()
        args = parser.parse_args(["export", "ls"])
        args.func(args)

        out = capsys.readouterr().out
        assert out.splitlines() == ["other-exportable", "some-exportable"]

    def test_lists_nothing_when_registry_empty(self, capsys):
        with patch.object(exportable_parser, "exportable_registry", {}):
            parser = _build_export_parser()
            args = parser.parse_args(["export", "ls"])
            args.func(args)

        out = capsys.readouterr().out
        assert out == ""


class TestExportMainPrintsContent:

    def test_prints_content_of_known_exportable(
        self, _fake_registry, capsys
    ):
        parser = _build_export_parser()
        args = parser.parse_args(["export", "some-exportable"])
        args.func(args)

        out = capsys.readouterr().out
        assert "fake exportable content for some-exportable" in out


class TestExportMainUnknownExportable:

    def test_exits_on_unknown_exportable(self, _fake_registry):
        parser = _build_export_parser()
        args = parser.parse_args(["export", "does-not-exist"])

        with pytest.raises(SystemExit):
            args.func(args)

    def test_logs_critical_on_unknown_exportable(
        self, _fake_registry, caplog
    ):
        parser = _build_export_parser()
        args = parser.parse_args(["export", "does-not-exist"])

        with caplog.at_level(logging.CRITICAL, logger=LOGGER_NAME):
            with pytest.raises(SystemExit):
                args.func(args)

        assert any(
            rec.levelno == logging.CRITICAL for rec in caplog.records
        )
        assert any(
            "does-not-exist" in rec.message for rec in caplog.records
        )
