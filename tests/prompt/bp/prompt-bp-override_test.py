"""
prompt-bp-override_test.py

Unit Tests (using pytest) for: override_exportable()
"""

import pytest

from kaye_engine.consumer import register_consumer
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import create_blueprint
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.blueprint.registry import (
    blueprint_registry,
    override_exportable,
    register_blueprint,
)
from kaye_engine.skill.select import select_exportables

from tests.consumer_helper import TEST_CONSUMER, isolated_consumers

_NAMES = ("ovr-base", "ovr-core", "ovr-top", "ovr-internal")


@pytest.fixture(autouse=True)
def _registered():
    with isolated_consumers():
        register_consumer("Other Package", "other-pkg", "3.0.0")
        register_blueprint(
            "ovr-core", create_blueprint(), is_exportable=False
        )
        register_blueprint(
            "ovr-base",
            create_blueprint(),
            consumer=TEST_CONSUMER,
            always_apply=True,
            render_profile=RenderProfile(sparseness=3),
        )
        register_blueprint(
            "ovr-top",
            create_blueprint(dependencies=["ovr-base"]),
            consumer=TEST_CONSUMER,
        )
        register_blueprint(
            "ovr-internal", create_blueprint(), is_exportable=False
        )
        yield
        for name in _NAMES:
            blueprint_registry.pop(name, None)
            exportable_registry.pop(name, None)


class TestOverride:

    def test_skill_moves_to_overriding_consumer(_):
        new = create_blueprint(dependencies=["ovr-core"])

        override_exportable("ovr-base", new, consumer="other-pkg")

        assert exportable_registry["ovr-base"].consumer == "other-pkg"
        assert select_exportables(consumer="other-pkg")[0].canonical_name == (
            "ovr-base"
        )
        assert "ovr-base" not in {
            e.canonical_name
            for e in select_exportables(consumer=TEST_CONSUMER)
        }

    def test_blueprint_replaced_in_both_registries(_):
        new = create_blueprint(dependencies=["ovr-core"])

        entry = override_exportable("ovr-base", new, consumer="other-pkg")

        assert entry.blueprint is new
        assert blueprint_registry["ovr-base"].blueprint is new
        assert exportable_registry["ovr-base"] is entry

    def test_render_profile_set_with_blueprint(_):
        profile = RenderProfile(sparseness=9)

        entry = override_exportable(
            "ovr-base",
            create_blueprint(),
            consumer="other-pkg",
            render_profile=profile,
        )

        assert entry.render_profile is profile

    def test_render_profile_kept_when_omitted(_):
        entry = override_exportable(
            "ovr-base", create_blueprint(), consumer="other-pkg"
        )

        assert entry.render_profile.sparseness == 3
        assert entry.always_apply is True

    def test_dependents_see_the_new_blueprint(_):
        new = create_blueprint(dependencies=["ovr-core"])

        override_exportable("ovr-base", new, consumer="other-pkg")

        assert blueprint_registry["ovr-top"].blueprint.dependencies == (
            "ovr-base",
        )


class TestRefused:

    def test_unknown_dependency_raises_and_changes_nothing(_):
        before = blueprint_registry["ovr-base"].blueprint

        with pytest.raises(ValueError, match="no-such-dep"):
            override_exportable(
                "ovr-base",
                create_blueprint(dependencies=["no-such-dep"]),
                consumer="other-pkg",
            )

        entry = blueprint_registry["ovr-base"]
        assert entry.blueprint is before
        assert entry.consumer == TEST_CONSUMER

    def test_direct_cycle_raises(_):
        with pytest.raises(ValueError, match="cycle"):
            override_exportable(
                "ovr-base",
                create_blueprint(dependencies=["ovr-base"]),
                consumer="other-pkg",
            )

    def test_indirect_cycle_raises(_):
        with pytest.raises(ValueError, match="cycle"):
            override_exportable(
                "ovr-base",
                create_blueprint(dependencies=["ovr-top"]),
                consumer="other-pkg",
            )

    def test_unregistered_name_raises(_):
        with pytest.raises(ValueError, match="no-such-skill"):
            override_exportable(
                "no-such-skill", create_blueprint(), consumer="other-pkg"
            )

    def test_non_exportable_raises(_):
        with pytest.raises(ValueError, match="ovr-internal"):
            override_exportable(
                "ovr-internal", create_blueprint(), consumer="other-pkg"
            )

    def test_unknown_consumer_raises(_):
        with pytest.raises(ValueError, match="nobody"):
            override_exportable(
                "ovr-base", create_blueprint(), consumer="nobody"
            )
        assert exportable_registry["ovr-base"].consumer == TEST_CONSUMER
