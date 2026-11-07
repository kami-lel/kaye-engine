"""
cli_setup_guard_test.py

Unit Tests (using pytest) for:

- check_corpus_setup_for_cli, note_empty_registry_for_cli
"""

import logging
from unittest.mock import patch

from kaye_engine import LOGGER_NAME
from kaye_engine.cli.cli_setup_guard import (
    check_corpus_setup_for_cli,
    note_empty_registry_for_cli,
)


class TestCheckCorpusSetupForCliNoCorpusTree:

    def test_logs_error(_, caplog):
        with patch(
            "kaye_engine.cli.cli_setup_guard.get_corpus_tree",
            side_effect=ValueError,
        ):
            with patch(
                "kaye_engine.cli.cli_setup_guard.blueprint_registry",
                {"chat": object()},
            ):
                with caplog.at_level(logging.ERROR, logger=LOGGER_NAME):
                    check_corpus_setup_for_cli()

        assert any(rec.levelno == logging.ERROR for rec in caplog.records)
        assert any(
            "no corpus tree loaded" in rec.message
            and "load_corpus_tree()" in rec.message
            for rec in caplog.records
        )


class TestCheckCorpusSetupForCliNoBlueprints:

    def test_logs_error(_, caplog):
        with patch(
            "kaye_engine.cli.cli_setup_guard.get_corpus_tree",
        ):
            with patch(
                "kaye_engine.cli.cli_setup_guard.blueprint_registry", {}
            ):
                with caplog.at_level(logging.ERROR, logger=LOGGER_NAME):
                    check_corpus_setup_for_cli()

        assert any(rec.levelno == logging.ERROR for rec in caplog.records)
        assert any(
            "no blueprints registered" in rec.message
            for rec in caplog.records
        )


class TestNoteEmptyRegistryForCli:

    def test_logs_one_note_naming_the_kind(_, caplog):
        with caplog.at_level(1, logger=LOGGER_NAME):
            note_empty_registry_for_cli("affordances")

        assert [rec.levelname for rec in caplog.records] == ["NOTE"]
        assert "no affordances registered" in caplog.records[0].message

    def test_logs_no_error(_, caplog):
        with caplog.at_level(1, logger=LOGGER_NAME):
            note_empty_registry_for_cli("variants")

        assert not any(rec.levelno >= logging.ERROR for rec in caplog.records)
