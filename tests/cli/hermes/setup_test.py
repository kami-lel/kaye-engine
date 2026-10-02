"""
tests/cli/hermes/setup_test.py

Unit Tests (using pytest) for:

- setup_hermes_cli
- get_hermes_soul_blueprint_name
- get_hermes_profile_blueprint_names
"""

from unittest.mock import patch

import pytest

from kaye_engine.cli import hermes
from kaye_engine.cli.hermes.setup import (
    get_hermes_profile_blueprint_names,
    get_hermes_soul_blueprint_name,
    setup_hermes_cli,
)

_REGISTRY = {"chat": object(), "kaye-chat": object(), "ria-chat": object()}


@pytest.fixture(autouse=True)
def _isolate_globals():
    saved = (
        hermes._soul_blueprint_name,
        hermes._profile_blueprint_names,
    )
    with patch("kaye_engine.cli.hermes.setup.blueprint_registry", _REGISTRY):
        yield
    (
        hermes._soul_blueprint_name,
        hermes._profile_blueprint_names,
    ) = saved


class TestSetup:

    def test_round_trip(_):
        setup_hermes_cli(
            "chat", {"kaye": "kaye-chat", "ria": "ria-chat"}
        )
        assert get_hermes_soul_blueprint_name() == "chat"
        assert get_hermes_profile_blueprint_names() == {
            "kaye": "kaye-chat",
            "ria": "ria-chat",
        }

    def test_unknown_soul_blueprint_exits(_):
        with pytest.raises(SystemExit) as info:
            setup_hermes_cli("nope", {})
        assert info.value.code == 1

    def test_unknown_profile_blueprint_exits(_):
        with pytest.raises(SystemExit) as info:
            setup_hermes_cli("chat", {"zin": "nope"})
        assert info.value.code == 1


class TestUnsetGetters:

    @pytest.mark.parametrize(
        "getter",
        (
            get_hermes_soul_blueprint_name,
            get_hermes_profile_blueprint_names,
        ),
    )
    def test_exits_one(_, getter):
        hermes._soul_blueprint_name = None
        hermes._profile_blueprint_names = None
        with pytest.raises(SystemExit) as info:
            getter()
        assert info.value.code == 1
