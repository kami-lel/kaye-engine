"""
cli_setup_guard_test.py

Unit Tests (using pytest) for:

- check_corpus_setup_for_cli
"""

import logging
from unittest.mock import patch

from kaye_engine import LOGGER_NAME
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli


class TestCheckCorpusSetupForCliNoCorpusTree:

    def test_logs_error(_, caplog):
        with patch(
            "kaye_engine.cli.cli_setup_guard.get_default_corpus_tree",
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
            "no corpus tree loaded" in rec.message for rec in caplog.records
        )


class TestCheckCorpusSetupForCliNoBlueprints:

    def test_logs_error(_, caplog):
        with patch(
            "kaye_engine.cli.cli_setup_guard.get_default_corpus_tree",
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
