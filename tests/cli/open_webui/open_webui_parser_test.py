"""
open_webui_parser_test.py

Unit Tests (using pytest) for:

register_sync_open_webui_skills_parser
"""

from argparse import ArgumentParser
from unittest.mock import MagicMock, patch

import pytest

from kaye_engine.cli.open_webui import parser as owu_parser
from kaye_engine.cli.open_webui.sync import SyncSummary


# auxiliaries  #################################################################
def _build_root_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    owu_parser.register_sync_open_webui_skills_parser(subparser)
    return root_parser


def _run(argv):
    args = _build_root_parser().parse_args(argv)
    args.func(args)


@pytest.fixture(autouse=True)
def _no_corpus_setup_guard(monkeypatch):
    monkeypatch.setattr(owu_parser, "check_corpus_setup_for_cli", lambda: None)
    monkeypatch.delenv(owu_parser.API_KEY_ENV_VAR, raising=False)


@pytest.fixture
def _fakes():
    with patch.object(owu_parser, "OpenWebUIClient") as client_cls, \
            patch.object(owu_parser, "sync_skills") as sync_mock:
        sync_mock.return_value = SyncSummary()
        yield client_cls, sync_mock


# pytest  ######################################################################
class TestRegistration:

    def test_registers_full_name_and_alias(_):
        for name in ("sync-open-webui-skills", "o"):
            args = _build_root_parser().parse_args([name])
            assert callable(args.func)

    def test_rejects_old_name(_):
        with pytest.raises(SystemExit):
            _build_root_parser().parse_args(["upsert-open-webui-skills"])


class TestBaseUrl:

    def test_defaults_to_localhost(_, _fakes):
        client_cls, _sync = _fakes
        _run(["o", "--api-key", "k"])

        client_cls.assert_called_once_with("http://localhost:8080", "k")

    def test_flag_overrides_default(_, _fakes):
        client_cls, _sync = _fakes
        _run(["o", "--api-key", "k", "--base-url", "http://h:1"])

        client_cls.assert_called_once_with("http://h:1", "k")


class TestApiKey:

    def test_key_from_env(_, _fakes, monkeypatch):
        client_cls, _sync = _fakes
        monkeypatch.setenv("OWU_API_KEY", "env-key")
        _run(["o"])

        assert client_cls.call_args.args[1] == "env-key"

    def test_flag_overrides_env(_, _fakes, monkeypatch):
        client_cls, _sync = _fakes
        monkeypatch.setenv("OWU_API_KEY", "env-key")
        _run(["o", "--api-key", "flag-key"])

        assert client_cls.call_args.args[1] == "flag-key"

    def test_missing_key_errors_and_skips_sync(_, _fakes):
        _client_cls, sync_mock = _fakes
        with pytest.raises(SystemExit) as info:
            _run(["o"])

        assert info.value.code == 2
        sync_mock.assert_not_called()


class TestFlagWiring:

    def test_flags_reach_executor(_, _fakes):
        client_cls, sync_mock = _fakes
        _run(["o", "--api-key", "k", "--dry-run", "--prune"])

        sync_mock.assert_called_once_with(
            client_cls.return_value, is_dry_run=True, should_prune=True
        )

    def test_flags_default_off(_, _fakes):
        client_cls, sync_mock = _fakes
        _run(["o", "--api-key", "k"])

        sync_mock.assert_called_once_with(
            client_cls.return_value, is_dry_run=False, should_prune=False
        )


class TestExitStatus:

    def test_failures_exit_non_zero(_, _fakes):
        _client_cls, sync_mock = _fakes
        sync_mock.return_value = SyncSummary(failed=[("a", MagicMock())])
        with pytest.raises(SystemExit) as info:
            _run(["o", "--api-key", "k"])

        assert info.value.code == 1

    def test_remote_fetch_failure_exits_non_zero(_, _fakes):
        _client_cls, sync_mock = _fakes
        sync_mock.side_effect = owu_parser.OpenWebUIError(401, "no")
        with pytest.raises(SystemExit) as info:
            _run(["o", "--api-key", "k"])

        assert info.value.code == 1

    def test_clean_run_returns_normally(_, _fakes):
        _run(["o", "--api-key", "k"])
