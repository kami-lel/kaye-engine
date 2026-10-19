"""
tests/cli/claude/claude_setup_test.py

test:
- get_marketplace_name, get_marketplace_folder_name: always the engine name
- setup_claude_cli: chat and coder names optional; getters exit 1 unset
"""

import pytest
from kaye_engine import PACKAGE_NAME
from kaye_engine.cli import claude
from kaye_engine.cli.claude.exportable_name import (
    get_claude_chat_exportable,
    get_claude_merged_coder_exportable,
)
from kaye_engine.cli.claude.plugin_marketplace_name import (
    get_marketplace_name,
)
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
    def test_is_engine_name(_, getter):
        assert getter() == PACKAGE_NAME == "kaye-engine"


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
