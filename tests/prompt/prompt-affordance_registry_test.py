"""
prompt-affordance_registry_test.py

Unit Tests (using pytest) for:

- register_affordance()
- get_affordance()
- Affordance.usage_sidecar_name / Affordance.lack_sidecar_name
"""

import pytest

from kaye_engine.prompt.affordance_registry import (
    Affordance,
    affordance_registry,
    get_affordance,
    register_affordance,
)


@pytest.fixture
def registered_names():
    names = []
    yield names
    for name in names:
        affordance_registry.pop(name, None)


# Pytest unit tests  ###########################################################
class TestRegisterAffordance:

    def test_dft(_, registered_names):
        entry = register_affordance("Claude Tool:Test")
        registered_names.append(entry.canonical_name)

        assert isinstance(entry, Affordance)
        assert entry.canonical_name == "Claude Tool:Test"
        assert affordance_registry["Claude Tool:Test"] is entry

    def test_duplicate_name(_, registered_names):
        entry = register_affordance("Claude Tool:TestDup")
        registered_names.append(entry.canonical_name)

        with pytest.raises(ValueError) as exec_info:
            register_affordance("Claude Tool:TestDup")

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "duplicate affordance registry name: Claude Tool:TestDup"


class TestGetAffordance:

    def test_known_name(_, registered_names):
        entry = register_affordance("Claude Tool:TestGet")
        registered_names.append(entry.canonical_name)

        assert get_affordance("Claude Tool:TestGet") is entry

    def test_unknown_name(_):
        with pytest.raises(KeyError):
            get_affordance("Claude Tool:NoSuchName")


class TestSidecarNames:

    def test_usage_and_lack_sidecar_names(_, registered_names):
        entry = register_affordance("Claude Tool:TestSidecar")
        registered_names.append(entry.canonical_name)

        assert entry.usage_sidecar_name == "[Claude Tool:TestSidecar] Usage"
        assert entry.lack_sidecar_name == "[Claude Tool:TestSidecar] Lack"
