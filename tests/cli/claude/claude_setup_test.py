"""
tests/cli/claude/claude_setup_test.py

test:
- get_plugin_name, get_marketplace_name, get_marketplace_folder_name
  derive from the registered consumer
"""

import pytest
from kaye_engine.cli.claude.plugin_marketplace_name import (
    get_marketplace_name,
    get_plugin_name,
)
from kaye_engine.cli.claude.setup import get_marketplace_folder_name
from kaye_engine.consumer import register_consumer, set_entry_consumer

from tests.consumer_helper import isolated_consumers

_GETTERS = (get_plugin_name, get_marketplace_name, get_marketplace_folder_name)


@pytest.fixture(autouse=True)
def _isolate_globals():
    with isolated_consumers():
        yield


class TestDerivedNames:

    @pytest.mark.parametrize("getter", _GETTERS)
    def test_equals_canonical_name(_, getter):
        register_consumer("Some Proj", "some-proj", "1")
        set_entry_consumer("some-proj")
        assert getter() == "some-proj"

    @pytest.mark.parametrize("getter", _GETTERS)
    def test_exits_when_unregistered(_, getter):
        with pytest.raises(SystemExit) as info:
            getter()
        assert info.value.code == 1
