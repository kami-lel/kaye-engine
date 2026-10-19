"""
exportable_abbr_consumer_test.py

Unit Tests (using pytest) for: the consumer of each abbr group --
``set_abbr_group_consumer``, ``register_exportable_abbrs``
"""

from unittest.mock import patch

import pytest

from kaye_engine.abbr_collection import AbbrData, AbbrMeaning
from kaye_engine.abbr_collection.abbr_glossary_registry import (
    abbr_glossary_registry,
)
from kaye_engine.cli import exportable_abbr
from kaye_engine.cli.exportable_abbr import (
    ExportableAbbr,
    register_exportable_abbrs,
    set_abbr_group_consumer,
)
from kaye_engine.consumer import register_consumer
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import BlueprintRegistry, create_blueprint

from tests.consumer_helper import (
    TEST_CONSUMER,
    isolated_consumers,
    register_abbr_glossary,
)

_GLOSSARY = "test-glossary-owned"


@pytest.fixture(autouse=True)
def _isolate():
    data = AbbrData()
    with isolated_consumers(), patch.dict(
        exportable_registry, {}, clear=True
    ), patch(
        "kaye_engine.cli.exportable_abbr.get_abbr_data", return_value=data
    ), patch.object(
        exportable_abbr, "_abbr_group_consumer", ""
    ):
        register_consumer("Group Owner", "group-owner", "1")
        register_abbr_glossary(_GLOSSARY, True)
        with data:
            data.add_entry(
                AbbrMeaning("for example"),
                "e.g.",
                {"priority": 5, "tags": [_GLOSSARY], "wrap": "word"},
            )
        yield
        abbr_glossary_registry.pop(_GLOSSARY, None)


class TestUnclaimed:

    def test_only_glossary_groups_register(_):
        register_exportable_abbrs()

        assert "glossary-" + _GLOSSARY in exportable_registry
        assert all(name.startswith("glossary-") for name in exportable_registry)

    def test_glossary_group_takes_glossary_consumer(_):
        register_exportable_abbrs()

        group = exportable_registry["glossary-" + _GLOSSARY]
        assert group.consumer == TEST_CONSUMER


class TestClaimed:

    def test_claim_registers_tag_wrap_and_char_groups(_):
        set_abbr_group_consumer("group-owner")

        group = exportable_registry["abbr-starts-with-e"]
        assert isinstance(group, ExportableAbbr)
        assert group.consumer == "group-owner"
        assert exportable_registry["glossary-" + _GLOSSARY].consumer == (
            TEST_CONSUMER
        )

    def test_second_claim_raises(_):
        set_abbr_group_consumer("group-owner")

        with pytest.raises(ValueError, match="already claimed"):
            set_abbr_group_consumer("group-owner")

    def test_unknown_consumer_raises(_):
        with pytest.raises(ValueError, match="unregistered consumer"):
            set_abbr_group_consumer("nobody")

    def test_rebuild_replaces_abbr_group(_):
        set_abbr_group_consumer("group-owner")
        before = exportable_registry["abbr-starts-with-e"]

        register_exportable_abbrs()

        assert exportable_registry["abbr-starts-with-e"] is not before

    def test_rebuild_refuses_to_replace_other_exportable(_):
        exportable_registry["abbr-starts-with-e"] = BlueprintRegistry(
            canonical_name="abbr-starts-with-e",
            blueprint=create_blueprint(),
            consumer=TEST_CONSUMER,
        )

        with pytest.raises(ValueError, match="collides"):
            set_abbr_group_consumer("group-owner")
