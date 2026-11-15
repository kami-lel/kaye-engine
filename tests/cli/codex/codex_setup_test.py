"""
tests/cli/codex/codex_setup_test.py

test:
- setup_codex_cli: chat and coder names optional; getters exit 1 unset
- codex user-system-prompt: prints the configured Chat or merged Coder
"""

from argparse import ArgumentParser
from unittest.mock import MagicMock, patch

import pytest
from kaye_engine import setup_codex_cli
from kaye_engine.cli import codex
from kaye_engine.cli.codex.exportable_name import (
    get_codex_chat_exportable,
    get_codex_merged_coder_exportable,
)
from kaye_engine.cli.codex.main import register_cli_codex_parser
from kaye_engine.cli.codex.user_prompt import parser as usp_parser


@pytest.fixture(autouse=True)
def _isolate_globals():
    saved = (codex._chat_exportable_name, codex._merged_coder_exportable_name)
    yield
    codex._chat_exportable_name, codex._merged_coder_exportable_name = saved


class TestStructure:

    def test_usp_aliases_and_coder_flag(_):
        root = ArgumentParser()
        register_cli_codex_parser(root.add_subparsers())

        args = root.parse_args(["o", "usp", "-c"])

        assert args.coder is True
        assert callable(root.parse_args(["codex", "user-system-prompt"]).func)


class TestHeader:

    def test_setup_without_names_is_allowed(_):
        setup_codex_cli()

        assert codex._chat_exportable_name is None
        assert codex._merged_coder_exportable_name is None

    @pytest.mark.parametrize(
        "getter",
        [get_codex_chat_exportable, get_codex_merged_coder_exportable],
    )
    def test_unset_name_exits_one_naming_setup(_, getter, caplog):
        setup_codex_cli()

        with pytest.raises(SystemExit) as info:
            getter()

        assert info.value.code == 1
        assert "setup_codex_cli" in caplog.text

    def test_unknown_name_exits_one(_, caplog):
        setup_codex_cli("no-such-exportable")

        with pytest.raises(SystemExit):
            get_codex_chat_exportable()

        assert "unknown exportable" in caplog.text


class TestContent:

    @pytest.mark.parametrize(
        "use_coder, expected", [(False, "chat"), (True, "coder")]
    )
    def test_renders_configured_exportable(_, use_coder, expected):
        setup_codex_cli("chat", "coder")
        fakes = {
            name: MagicMock(**{"content.return_value": name})
            for name in ("chat", "coder")
        }

        with patch(
            "kaye_engine.cli.codex.exportable_name.get_exportable",
            side_effect=fakes.__getitem__,
        ):
            prompt = usp_parser.generate_codex_user_system_prompt(
                use_coder=use_coder
            )

        assert prompt == expected
