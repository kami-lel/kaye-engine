"""
prompt-bp-render_profile_registry_test.py

Unit Tests (using pytest) for:

- register_render_profile()
- RenderProfileEntry
"""

import dataclasses

import pytest

from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.blueprint.render_profile_registry import (
    RenderProfileEntry,
    register_render_profile,
    render_profile_registry,
)
from tests.consumer_helper import isolated_render_profiles


class TestRegister:  ############################################################

    def test_stores_profile_and_remark(_):
        with isolated_render_profiles():
            profile = RenderProfile(sparseness=0)
            entry = register_render_profile("a", profile, "the a one")
            assert render_profile_registry["a"] is entry
            assert entry.name == "a"
            assert entry.profile is profile
            assert entry.remark == "the a one"

    def test_remark_defaults_to_empty_str(_):
        with isolated_render_profiles():
            entry = register_render_profile("a", RenderProfile())
            assert entry.remark == ""

    def test_keeps_registration_order(_):
        with isolated_render_profiles():
            register_render_profile("b", RenderProfile())
            register_render_profile("a", RenderProfile())
            assert list(render_profile_registry) == ["b", "a"]

    def test_duplicate_name_raises(_):
        with isolated_render_profiles():
            register_render_profile("a", RenderProfile())
            with pytest.raises(ValueError, match="a"):
                register_render_profile("a", RenderProfile())

    @pytest.mark.parametrize("remark", [None, 1, b"x", ["x"]])
    def test_non_str_remark_raises(_, remark):
        with isolated_render_profiles():
            with pytest.raises(TypeError):
                register_render_profile("a", RenderProfile(), remark)
            assert "a" not in render_profile_registry


class TestIsolation:  ###########################################################

    def test_restores_registry_on_exit(_):
        before = dict(render_profile_registry)
        with isolated_render_profiles():
            assert not render_profile_registry
            register_render_profile("temp", RenderProfile())
        assert render_profile_registry == before


class TestEntry:  ###############################################################

    def test_is_frozen(_):
        entry = RenderProfileEntry(name="a", profile=RenderProfile())
        with pytest.raises(dataclasses.FrozenInstanceError):
            entry.remark = "changed"
