"""
tests/consumer_test.py

test:
- register_consumer, get_consumer, iter_consumers
- set_entry_consumer and the get_consumer_* getters reading it
- every exportable registration naming a registered consumer
"""

import pytest

from kaye_engine.abbr_collection import register_abbr_glossary
from kaye_engine.consumer import (
    check_consumer,
    get_consumer,
    get_consumer_canonical_name,
    get_consumer_display_name,
    get_consumer_version,
    iter_consumers,
    register_consumer,
    set_entry_consumer,
)
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import create_blueprint
from kaye_engine.prompt.blueprint.registry import (
    blueprint_registry,
    register_blueprint,
)

from tests.consumer_helper import isolated_consumers

_GETTERS = (
    get_consumer_display_name,
    get_consumer_canonical_name,
    get_consumer_version,
)


@pytest.fixture(autouse=True)
def _isolate():
    with isolated_consumers():
        yield


class TestRegisterConsumer:

    def test_round_trip(_):
        record = register_consumer("Some Proj", "some-proj", "1.2.3")

        assert get_consumer("some-proj") is record
        assert record.display_name == "Some Proj"
        assert record.version == "1.2.3"

    def test_two_consumers_side_by_side(_):
        register_consumer("A", "a", "1")
        register_consumer("B", "b", "2")

        names = [c.canonical_name for c in iter_consumers()]
        assert names[-2:] == ["a", "b"]
        assert get_consumer("a").version == "1"
        assert get_consumer("b").version == "2"

    def test_repeated_canonical_name_raises(_):
        register_consumer("A", "a", "1")

        with pytest.raises(ValueError, match="duplicate consumer"):
            register_consumer("A again", "a", "2")
        assert get_consumer("a").display_name == "A"

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

    def test_unknown_consumer_raises(_):
        with pytest.raises(ValueError, match="unregistered consumer"):
            get_consumer("nobody")


class TestEntryConsumer:

    def test_getters_read_entry_consumer(_):
        register_consumer("A", "a", "1")
        register_consumer("B", "b", "2")
        set_entry_consumer("b")

        assert get_consumer_display_name() == "B"
        assert get_consumer_canonical_name() == "b"
        assert get_consumer_version() == "2"

    def test_later_call_wins(_):
        register_consumer("A", "a", "1")
        register_consumer("B", "b", "2")
        set_entry_consumer("a")
        set_entry_consumer("b")

        assert get_consumer_canonical_name() == "b"

    def test_unknown_entry_consumer_raises(_):
        with pytest.raises(ValueError):
            set_entry_consumer("nobody")

    @pytest.mark.parametrize("getter", _GETTERS)
    def test_exits_when_unset(_, getter):
        register_consumer("A", "a", "1")

        with pytest.raises(SystemExit) as info:
            getter()
        assert info.value.code == 1


class TestExportableNamesConsumer:

    @pytest.fixture(autouse=True)
    def _cleanup(_):
        yield
        for name in ("test-consumer-bp", "test-consumer-internal"):
            blueprint_registry.pop(name, None)
            exportable_registry.pop(name, None)

    def test_exportable_without_consumer_raises(_):
        with pytest.raises(ValueError, match="unregistered consumer"):
            register_blueprint("test-consumer-bp", create_blueprint())
        assert "test-consumer-bp" not in blueprint_registry

    def test_exportable_with_unknown_consumer_raises(_):
        with pytest.raises(ValueError, match="nobody"):
            register_blueprint(
                "test-consumer-bp", create_blueprint(), consumer="nobody"
            )

    def test_exportable_records_consumer(_):
        register_consumer("A", "a", "1")

        reg = register_blueprint(
            "test-consumer-bp", create_blueprint(), consumer="a"
        )

        assert reg.consumer == "a"
        assert exportable_registry["test-consumer-bp"].consumer == "a"

    def test_internal_blueprint_needs_no_consumer(_):
        reg = register_blueprint(
            "test-consumer-internal", create_blueprint(), is_exportable=False
        )

        assert reg.consumer == ""

    def test_exportable_glossary_without_consumer_raises(_):
        with pytest.raises(ValueError, match="unregistered consumer"):
            register_abbr_glossary("test-consumer-glossary", True)

    def test_check_consumer_returns_name(_):
        register_consumer("A", "a", "1")

        assert check_consumer("a") == "a"
