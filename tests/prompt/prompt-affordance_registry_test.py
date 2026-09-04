"""
prompt-affordance_registry_test.py

Unit Tests (using pytest) for:

- register_variant()
- Affordance.usage_sidecar_name
- Affordance.fallback_sidecar_name
- Variant.usage_sidecar_name
- Variant.lack_sidecar_name
"""

import pytest
from kaye_engine.prompt.affordance_registry import (
    Affordance,
    Variant,
    affordance_registry,
    register_variant,
    variant_registry,
)


@pytest.fixture
def registered_names():
    names = []
    yield names
    for name in names:
        variant_registry.pop(name, None)


@pytest.fixture
def registered_affordance_names():
    names = []
    yield names
    for name in names:
        affordance_registry.pop(name, None)


# Pytest unit tests  ###########################################################
class TestRegisterVariant:

    def test_dft(_, registered_names, registered_affordance_names):
        entry = register_variant("Claude Tool:Test", "Claude Tool:Family")
        registered_names.append(entry.canonical_name)
        registered_affordance_names.append(entry.affordance_name)

        assert isinstance(entry, Variant)
        assert entry.canonical_name == "Claude Tool:Test"
        assert entry.affordance_name == "Claude Tool:Family"
        assert variant_registry["Claude Tool:Test"] is entry

    def test_auto_creates_missing_affordance(
        _, registered_names, registered_affordance_names
    ):
        entry = register_variant(
            "Claude Tool:TestAuto", "Claude Tool:FamilyAuto"
        )
        registered_names.append(entry.canonical_name)
        registered_affordance_names.append(entry.affordance_name)

        assert isinstance(
            affordance_registry["Claude Tool:FamilyAuto"], Affordance
        )

    def test_reuses_existing_affordance(
        _, registered_names, registered_affordance_names
    ):
        first = register_variant("Claude Tool:TestA", "Claude Tool:FamilyB")
        second = register_variant("Claude Tool:TestB", "Claude Tool:FamilyB")
        registered_names.extend([first.canonical_name, second.canonical_name])
        registered_affordance_names.append("Claude Tool:FamilyB")

        assert first.affordance_name == second.affordance_name
        assert list(affordance_registry).count("Claude Tool:FamilyB") == 1

    def test_duplicate_name(_, registered_names, registered_affordance_names):
        entry = register_variant("Claude Tool:TestDup", "Claude Tool:FamilyDup")
        registered_names.append(entry.canonical_name)
        registered_affordance_names.append(entry.affordance_name)

        with pytest.raises(ValueError) as exec_info:
            register_variant("Claude Tool:TestDup", "Claude Tool:FamilyDup")

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "duplicate variant registry name: Claude Tool:TestDup"


class TestSidecarNames:

    def test_usage_sidecar_name(
        _, registered_names, registered_affordance_names
    ):
        entry = register_variant(
            "Claude Tool:TestSidecar", "Claude Tool:FamilySidecar"
        )
        registered_names.append(entry.canonical_name)
        registered_affordance_names.append(entry.affordance_name)

        assert entry.usage_sidecar_name == "[Claude Tool:TestSidecar] Usage"

    def test_fallback_sidecar_name(
        _, registered_names, registered_affordance_names
    ):
        entry = register_variant(
            "Claude Tool:TestFallback", "Claude Tool:FamilyFallback"
        )
        registered_names.append(entry.canonical_name)
        registered_affordance_names.append(entry.affordance_name)

        affordance = affordance_registry[entry.affordance_name]
        assert (
            affordance.fallback_sidecar_name
            == "[Claude Tool:FamilyFallback] Fallback"
        )

    def test_affordance_usage_sidecar_name(
        _, registered_names, registered_affordance_names
    ):
        entry = register_variant(
            "Claude Tool:TestAffUsage", "Claude Tool:FamilyAffUsage"
        )
        registered_names.append(entry.canonical_name)
        registered_affordance_names.append(entry.affordance_name)

        affordance = affordance_registry[entry.affordance_name]
        assert (
            affordance.usage_sidecar_name
            == "[Claude Tool:FamilyAffUsage] Usage"
        )

    def test_variant_lack_sidecar_name(
        _, registered_names, registered_affordance_names
    ):
        entry = register_variant(
            "Claude Tool:TestLack", "Claude Tool:FamilyLack"
        )
        registered_names.append(entry.canonical_name)
        registered_affordance_names.append(entry.affordance_name)

        assert entry.lack_sidecar_name == "[Claude Tool:TestLack] Lack"
