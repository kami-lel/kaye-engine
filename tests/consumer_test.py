"""
tests/consumer_test.py

test:
- register_consumer
- get_consumer_display_name, get_consumer_canonical_name,
  get_consumer_version
"""

import pytest
from kaye_engine import consumer
from kaye_engine.consumer import (
    get_consumer_canonical_name,
    get_consumer_display_name,
    get_consumer_version,
    register_consumer,
)

_GETTERS = (
    get_consumer_display_name,
    get_consumer_canonical_name,
    get_consumer_version,
)


@pytest.fixture(autouse=True)
def _isolate_globals():
    saved = (
        consumer._display_name,
        consumer._canonical_name,
        consumer._version,
    )
    yield
    (
        consumer._display_name,
        consumer._canonical_name,
        consumer._version,
    ) = saved


class TestRegisterConsumer:

    def test_round_trip(_):
        register_consumer("Some Proj", "some-proj", "1.2.3")
        assert get_consumer_display_name() == "Some Proj"
        assert get_consumer_canonical_name() == "some-proj"
        assert get_consumer_version() == "1.2.3"

    def test_repeated_call_overwrites(_):
        register_consumer("A", "a", "1")
        register_consumer("B", "b", "2")
        assert get_consumer_canonical_name() == "b"

    @pytest.mark.parametrize(
        "canonical_name", ["Some-Proj", "some_proj", "-a", "a-", "a--b", ""]
    )
    def test_non_kebab_raises(_, canonical_name):
        with pytest.raises(ValueError):
            register_consumer("X", canonical_name, "1")

    @pytest.mark.parametrize("bad", ["", "  ", None, 1])
    def test_bad_display_name_or_version_raises(_, bad):
        with pytest.raises(ValueError):
            register_consumer(bad, "x", "1")
        with pytest.raises(ValueError):
            register_consumer("X", "x", bad)

    def test_failed_call_keeps_previous(_):
        register_consumer("A", "a", "1")
        with pytest.raises(ValueError):
            register_consumer("B", "Bad Name", "2")
        assert get_consumer_display_name() == "A"


class TestUnsetGetters:

    @pytest.mark.parametrize("getter", _GETTERS)
    def test_exits_when_unregistered(_, getter):
        consumer._display_name = None
        consumer._canonical_name = None
        consumer._version = None
        with pytest.raises(SystemExit) as info:
            getter()
        assert info.value.code == 1
