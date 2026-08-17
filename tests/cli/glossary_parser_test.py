"""
glossary_parser_test.py

Unit Tests (using pytest) for:

_glossary_main, register_glossary_parser
"""

import logging
from argparse import ArgumentParser
from unittest.mock import patch

import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.cli import glossary_parser


# auxiliaries  ##################################################################
def _build_glossary_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    glossary_parser.register_glossary_parser(subparser)
    return root_parser


@pytest.fixture(autouse=True)
def _no_corpus_setup_guard():
    with patch.object(
        glossary_parser, "check_corpus_setup_for_cli", lambda: None
    ):
        yield


@pytest.fixture
def _fake_registry():
    registry = {"some-glossary": object(), "other-glossary": object()}
    with patch.object(glossary_parser, "abbr_glossary_registry", registry):
        yield registry


# pytest  ######################################################################
class TestRegisterGlossaryParser:

    def test_registers_glossary_subcommand(self):
        parser = _build_glossary_parser()
        args = parser.parse_args(["glossary", "some-glossary"])

        assert args.GLOSSARY == "some-glossary"
        assert args.func is glossary_parser._glossary_main

    def test_registers_g_alias(self):
        parser = _build_glossary_parser()
        args = parser.parse_args(["g", "some-glossary"])

        assert args.GLOSSARY == "some-glossary"


class TestGlossaryMainLs:

    def test_lists_registered_glossaries_sorted(
        self, _fake_registry, capsys
    ):
        parser = _build_glossary_parser()
        args = parser.parse_args(["glossary", "ls"])
        args.func(args)

        out = capsys.readouterr().out
        assert out.splitlines() == ["other-glossary", "some-glossary"]

    def test_lists_nothing_when_registry_empty(self, capsys):
        with patch.object(glossary_parser, "abbr_glossary_registry", {}):
            parser = _build_glossary_parser()
            args = parser.parse_args(["glossary", "ls"])
            args.func(args)

        out = capsys.readouterr().out
        assert out == ""


class TestGlossaryMainPrintsContent:

    def test_prints_content_of_known_glossary(self, _fake_registry, capsys):
        parser = _build_glossary_parser()
        args = parser.parse_args(["glossary", "some-glossary"])

        with patch.object(
            glossary_parser,
            "get_abbr_glossary",
            lambda name: _fake_registry[name],
        ), patch.object(
            glossary_parser,
            "gen_glossary_content_lines",
            lambda name: ["- fake entry for " + name],
        ):
            args.func(args)

        out = capsys.readouterr().out
        assert "fake entry for some-glossary" in out


class TestGlossaryMainUnknownGlossary:

    def test_exits_on_unknown_glossary(self, _fake_registry):
        parser = _build_glossary_parser()
        args = parser.parse_args(["glossary", "does-not-exist"])

        with pytest.raises(SystemExit):
            args.func(args)

    def test_logs_critical_on_unknown_glossary(self, _fake_registry, caplog):
        parser = _build_glossary_parser()
        args = parser.parse_args(["glossary", "does-not-exist"])

        with caplog.at_level(logging.CRITICAL, logger=LOGGER_NAME):
            with pytest.raises(SystemExit):
                args.func(args)

        assert any(
            rec.levelno == logging.CRITICAL for rec in caplog.records
        )
        assert any(
            "does-not-exist" in rec.message for rec in caplog.records
        )
