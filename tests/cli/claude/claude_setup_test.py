"""
tests/cli/claude/claude_setup_test.py

test:
- get_marketplace_name, get_marketplace_folder_name: the repo name, exit 1
  when unset
- setup_claude_cli: chat and coder names optional; getters exit 1 unset
"""

import pytest
from kaye_engine import repo
from kaye_engine.repo import set_repo_name
from kaye_engine.cli import claude
from kaye_engine.cli.claude.exportable_name import (
    get_claude_chat_exportable,
    get_claude_merged_coder_exportable,
)
from kaye_engine.cli.claude.plugin_marketplace_name import (
    get_marketplace_name,
)
from tests.consumer_helper import isolated_repo
from kaye_engine.cli.claude.setup import (
    get_marketplace_folder_name,
    setup_claude_cli,
)

_GETTERS = (get_marketplace_name, get_marketplace_folder_name)


@pytest.fixture(autouse=True)
def _isolate_globals():
    saved = (
        claude._chat_exportable_name,
        claude._merged_coder_exportable_name,
    )
    yield
    (
        claude._chat_exportable_name,
        claude._merged_coder_exportable_name,
    ) = saved


class TestMarketplaceNames:

    @pytest.mark.parametrize("getter", _GETTERS)
    @pytest.mark.parametrize("repo_name", ["kaye-library", "kaye-vault"])
    def test_is_repo_name(_, getter, repo_name):
        with isolated_repo():
            set_repo_name(repo_name)

            assert getter() == repo_name

    @pytest.mark.parametrize("getter", _GETTERS)
    def test_exits_one_when_repo_name_unset(_, getter, caplog):
        with isolated_repo():
            repo._repo_name = None
            with pytest.raises(SystemExit) as info:
                getter()

        assert info.value.code == 1
        assert "no repo name set" in caplog.text


class TestOptionalNames:

    def test_setup_without_names_is_allowed(_):
        setup_claude_cli()

        assert claude._chat_exportable_name is None
        assert claude._merged_coder_exportable_name is None

    @pytest.mark.parametrize(
        "getter",
        [get_claude_chat_exportable, get_claude_merged_coder_exportable],
    )
    def test_getter_exits_one_when_unset(_, getter, caplog):
        setup_claude_cli()

        with pytest.raises(SystemExit) as info:
            getter()

        assert info.value.code == 1
        assert "setup_claude_cli" in caplog.text


class TestBareCheckout:

    def test_check_exits_one_without_consumer(_, caplog):
        from kaye_engine.cli.claude.plugin_marketplace_name import (
            check_setup_for_claude_cli,
        )

        from tests.consumer_helper import isolated_consumers
        from kaye_engine import consumer as consumer_module

        with isolated_consumers():
            consumer_module._consumers.clear()
            with pytest.raises(SystemExit) as info:
                check_setup_for_claude_cli()

        assert info.value.code == 1
        assert "no consumer registered" in caplog.text
