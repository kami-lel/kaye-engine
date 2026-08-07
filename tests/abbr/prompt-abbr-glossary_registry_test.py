"""
prompt-abbr-glossary_registry_test.py

Unit Tests (using pytest) for:

- register_abbr_glossary()
- get_abbr_glossary()
- AbbrGlossaryRegistry
- AbbrData.add_entry() rejecting unregistered glossaries
- GlossaryNode rendering defaults driven by the registry
"""

import pytest

from kaye_engine.abbr_collection import AbbrData, AbbrMeaning
from kaye_engine.abbr_collection.abbr_glossary_registry import (
    AbbrGlossaryRegistry,
    abbr_glossary_registry,
    get_abbr_glossary,
    register_abbr_glossary,
)
from kaye_engine.prompt.dynamic_nodes import GlossaryNode


@pytest.fixture
def registered_names():
    names = []
    yield names
    for name in names:
        abbr_glossary_registry.pop(name, None)


class TestRegisterAbbrGlossary:  ###################################################

    def test_dft(_, registered_names):
        reg = register_abbr_glossary("test-glossary-dft")
        registered_names.append(reg.name)

        assert isinstance(reg, AbbrGlossaryRegistry)
        assert reg.name == "test-glossary-dft"
        assert reg.uses_numbered_list is False
        assert reg.is_sorted is False
        assert abbr_glossary_registry["test-glossary-dft"] is reg

    def test_flags(_, registered_names):
        reg = register_abbr_glossary(
            "test-glossary-flags",
            uses_numbered_list=True,
            is_sorted=True,
        )
        registered_names.append(reg.name)

        assert reg.uses_numbered_list is True
        assert reg.is_sorted is True

    def test_duplicate_name(_, registered_names):
        reg = register_abbr_glossary("test-glossary-dup")
        registered_names.append(reg.name)

        with pytest.raises(ValueError) as exec_info:
            register_abbr_glossary("test-glossary-dup")

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "duplicate abbr glossary registry name: test-glossary-dup"


class TestGetAbbrGlossary:  ########################################################

    def test_known_name(_, registered_names):
        reg = register_abbr_glossary("test-glossary-get")
        registered_names.append(reg.name)

        assert get_abbr_glossary("test-glossary-get") is reg

    def test_unknown_name(_):
        with pytest.raises(KeyError):
            get_abbr_glossary("test-glossary-no-such-name")


class TestAddEntryUnregisteredGlossary:  ###########################################

    def test_raises_on_unregistered_glossary(_):
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
                        "glossaries": ["test-glossary-unregistered"],
                    },
                )

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "unregistered abbr glossary: 'test-glossary-unregistered'"


class TestRenderingDefaults:  ###################################################

    def test_uses_numbered_list_default(_, registered_names):
        reg = register_abbr_glossary(
            "test-glossary-numbered", uses_numbered_list=True
        )
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
                    "glossaries": ["test-glossary-numbered"],
                },
            )

        testee = GlossaryNode(None, glossary_name="test-glossary-numbered")
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "kaye_engine.prompt.dynamic_nodes.glossary_node.get_abbr_data",
                lambda: data,
            )
            opt = testee.content_lines()

        print(opt)
        assert opt == ["1. e.g.:for example"]

    def test_is_sorted_default(_, registered_names):
        reg = register_abbr_glossary("test-glossary-sorted", is_sorted=True)
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
                    "glossaries": ["test-glossary-sorted"],
                },
            )
            data.add_entry(
                AbbrMeaning("id est"),
                "i.e.",
                {
                    "priority": 1,
                    "tags": [],
                    "wrap": "word",
                    "glossaries": ["test-glossary-sorted"],
                },
            )

        testee = GlossaryNode(None, glossary_name="test-glossary-sorted")
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "kaye_engine.prompt.dynamic_nodes.glossary_node.get_abbr_data",
                lambda: data,
            )
            opt = testee.content_lines()

        print(opt)
        assert opt == ["- i.e.:id est", "- e.g.:for example"]

    def test_explicit_override_wins(_, registered_names):
        reg = register_abbr_glossary(
            "test-glossary-override", uses_numbered_list=True
        )
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
                    "glossaries": ["test-glossary-override"],
                },
            )

        testee = GlossaryNode(None, glossary_name="test-glossary-override")
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "kaye_engine.prompt.dynamic_nodes.glossary_node.get_abbr_data",
                lambda: data,
            )
            opt = testee.content_lines(uses_numbered_list=False)

        print(opt)
        assert opt == ["- e.g.:for example"]

    def test_glossary_priority_threshold_omitted_renders_all(
        _, registered_names
    ):
        reg = register_abbr_glossary("test-glossary-threshold")
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
                    "glossaries": ["test-glossary-threshold"],
                },
            )
            data.add_entry(
                AbbrMeaning("id est"),
                "i.e.",
                {
                    "priority": 6,
                    "tags": [],
                    "wrap": "word",
                    "glossaries": ["test-glossary-threshold"],
                },
            )

        assert len(data.abbrs) == 2

        testee = GlossaryNode(None, glossary_name="test-glossary-threshold")
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "kaye_engine.prompt.dynamic_nodes.glossary_node.get_abbr_data",
                lambda: data,
            )
            opt = testee.content_lines()

        print(opt)
        assert opt == ["- e.g.:for example", "- i.e.:id est"]

    def test_glossary_priority_threshold_filters(_, registered_names):
        reg = register_abbr_glossary("test-glossary-threshold-filtered")
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
                    "glossaries": ["test-glossary-threshold-filtered"],
                },
            )
            data.add_entry(
                AbbrMeaning("id est"),
                "i.e.",
                {
                    "priority": 6,
                    "tags": [],
                    "wrap": "word",
                    "glossaries": ["test-glossary-threshold-filtered"],
                },
            )

        testee = GlossaryNode(
            None, glossary_name="test-glossary-threshold-filtered"
        )
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "kaye_engine.prompt.dynamic_nodes.glossary_node.get_abbr_data",
                lambda: data,
            )
            opt = testee.content_lines(glossary_priority_threshold=5)

        print(opt)
        assert opt == ["- e.g.:for example"]
