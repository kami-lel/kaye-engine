"""
prompt-abbr-group_registry_test.py

Unit Tests (using pytest) for:

- register_abbr_group()
- get_abbr_group()
- AbbrGroupRegistry
- AbbrData.add_entry() rejecting unregistered groups
- AbbrGroupNode rendering defaults driven by the registry
"""

import pytest

from kaye_engine.abbr_collection import AbbrData, AbbrMeaning
from kaye_engine.abbr_collection.abbr_group_registry import (
    AbbrGroupRegistry,
    register_abbr_group,
    get_abbr_group,
    abbr_group_registry,
)
from kaye_engine.prompt.dynamic_nodes import AbbrGroupNode


@pytest.fixture
def registered_names():
    names = []
    yield names
    for name in names:
        abbr_group_registry.pop(name, None)


class TestRegisterAbbrGroup:  ###################################################

    def test_dft(_, registered_names):
        reg = register_abbr_group("test-group-dft")
        registered_names.append(reg.name)

        assert isinstance(reg, AbbrGroupRegistry)
        assert reg.name == "test-group-dft"
        assert reg.uses_numbered_list is False
        assert reg.is_sorted is False
        assert reg.priority_threshold is None
        assert abbr_group_registry["test-group-dft"] is reg

    def test_flags(_, registered_names):
        reg = register_abbr_group(
            "test-group-flags",
            uses_numbered_list=True,
            is_sorted=True,
            priority_threshold=5,
        )
        registered_names.append(reg.name)

        assert reg.uses_numbered_list is True
        assert reg.is_sorted is True
        assert reg.priority_threshold == 5

    def test_priority_threshold_not_int_raises(_):
        with pytest.raises(TypeError):
            register_abbr_group("test-group-bad-threshold", priority_threshold="5")

    def test_duplicate_name(_, registered_names):
        reg = register_abbr_group("test-group-dup")
        registered_names.append(reg.name)

        with pytest.raises(ValueError) as exec_info:
            register_abbr_group("test-group-dup")

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "duplicate abbr group registry name: test-group-dup"


class TestGetAbbrGroup:  ########################################################

    def test_known_name(_, registered_names):
        reg = register_abbr_group("test-group-get")
        registered_names.append(reg.name)

        assert get_abbr_group("test-group-get") is reg

    def test_unknown_name(_):
        with pytest.raises(KeyError):
            get_abbr_group("test-group-no-such-name")


class TestAddEntryUnregisteredGroup:  ###########################################

    def test_raises_on_unregistered_group(_):
        data = AbbrData()

        with pytest.raises(ValueError) as exec_info:
            with data:
                data.add_entry(
                    AbbrMeaning("dummy", remark=None),
                    "dmy",
                    {
                        "priority": 0,
                        "tags": [],
                        "wrap": "word",
                        "groups": ["test-group-unregistered"],
                    },
                )

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "unregistered abbr group: 'test-group-unregistered'"


class TestRenderingDefaults:  ###################################################

    def test_uses_numbered_list_default(_, registered_names):
        reg = register_abbr_group("test-group-numbered", uses_numbered_list=True)
        registered_names.append(reg.name)

        data = AbbrData()
        with data:
            data.add_entry(
                AbbrMeaning("for example"),
                "e.g.",
                {
                    "priority": 5,
                    "tags": [],
                    "wrap": "word",
                    "groups": ["test-group-numbered"],
                },
            )

        testee = AbbrGroupNode(None, group_name="test-group-numbered")
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "kaye_engine.prompt.dynamic_nodes.abbr_group_node.get_abbr_data",
                lambda: data,
            )
            opt = testee.content_lines()

        print(opt)
        assert opt == ["1. e.g.:for example"]

    def test_is_sorted_default(_, registered_names):
        reg = register_abbr_group("test-group-sorted", is_sorted=True)
        registered_names.append(reg.name)

        data = AbbrData()
        with data:
            data.add_entry(
                AbbrMeaning("for example"),
                "e.g.",
                {
                    "priority": 5,
                    "tags": [],
                    "wrap": "word",
                    "groups": ["test-group-sorted"],
                },
            )
            data.add_entry(
                AbbrMeaning("id est"),
                "i.e.",
                {
                    "priority": 1,
                    "tags": [],
                    "wrap": "word",
                    "groups": ["test-group-sorted"],
                },
            )

        testee = AbbrGroupNode(None, group_name="test-group-sorted")
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "kaye_engine.prompt.dynamic_nodes.abbr_group_node.get_abbr_data",
                lambda: data,
            )
            opt = testee.content_lines()

        print(opt)
        assert opt == ["- i.e.:id est", "- e.g.:for example"]

    def test_explicit_override_wins(_, registered_names):
        reg = register_abbr_group("test-group-override", uses_numbered_list=True)
        registered_names.append(reg.name)

        data = AbbrData()
        with data:
            data.add_entry(
                AbbrMeaning("for example"),
                "e.g.",
                {
                    "priority": 5,
                    "tags": [],
                    "wrap": "word",
                    "groups": ["test-group-override"],
                },
            )

        testee = AbbrGroupNode(None, group_name="test-group-override")
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "kaye_engine.prompt.dynamic_nodes.abbr_group_node.get_abbr_data",
                lambda: data,
            )
            opt = testee.content_lines(uses_numbered_list=False)

        print(opt)
        assert opt == ["- e.g.:for example"]

    def test_priority_threshold_default(_, registered_names):
        reg = register_abbr_group("test-group-threshold", priority_threshold=5)
        registered_names.append(reg.name)

        data = AbbrData()
        with data:
            data.add_entry(
                AbbrMeaning("for example"),
                "e.g.",
                {
                    "priority": 5,
                    "tags": [],
                    "wrap": "word",
                    "groups": ["test-group-threshold"],
                },
            )
            data.add_entry(
                AbbrMeaning("id est"),
                "i.e.",
                {
                    "priority": 6,
                    "tags": [],
                    "wrap": "word",
                    "groups": ["test-group-threshold"],
                },
            )

        assert len(data.abbrs) == 2

        testee = AbbrGroupNode(None, group_name="test-group-threshold")
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "kaye_engine.prompt.dynamic_nodes.abbr_group_node.get_abbr_data",
                lambda: data,
            )
            opt = testee.content_lines()

        print(opt)
        assert opt == ["- e.g.:for example"]

    def test_priority_threshold_explicit_override_wins(_, registered_names):
        reg = register_abbr_group("test-group-threshold-override")
        registered_names.append(reg.name)

        data = AbbrData()
        with data:
            data.add_entry(
                AbbrMeaning("for example"),
                "e.g.",
                {
                    "priority": 5,
                    "tags": [],
                    "wrap": "word",
                    "groups": ["test-group-threshold-override"],
                },
            )
            data.add_entry(
                AbbrMeaning("id est"),
                "i.e.",
                {
                    "priority": 6,
                    "tags": [],
                    "wrap": "word",
                    "groups": ["test-group-threshold-override"],
                },
            )

        testee = AbbrGroupNode(None, group_name="test-group-threshold-override")
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "kaye_engine.prompt.dynamic_nodes.abbr_group_node.get_abbr_data",
                lambda: data,
            )
            opt = testee.content_lines(priority_threshold=5)

        print(opt)
        assert opt == ["- e.g.:for example"]
