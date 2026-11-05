"""
tests/cli/claude/surface_parser_test.py

Unit Tests (using pytest) for:

- build_surface_parent_parser
- resolve_render_profile (the --surface merge)
"""

from argparse import ArgumentParser

import pytest

from kaye_engine.cli.claude.surface_parser import build_surface_parent_parser
from kaye_engine.cli.render_profile_parser import (
    build_render_profile_parent_parser,
    resolve_render_profile,
)
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.blueprint.render_profile_registry import (
    register_render_profile,
)
from tests.consumer_helper import isolated_render_profiles


@pytest.fixture(name="four_profiles")
def fixture_four_profiles():
    with isolated_render_profiles():
        for name in ("chat", "cowork", "code", "vsc"):
            register_render_profile(
                name, RenderProfile(conditional_sidecars=("[" + name + "]",))
            )
        yield


def _build_parser(default):
    return ArgumentParser(parents=[build_surface_parent_parser(default)])


# Pytest unit tests  ###########################################################
@pytest.mark.usefixtures("four_profiles")
class TestSurfaceFlag:

    def test_default_applied_when_omitted(_):
        args = _build_parser(("chat", "cowork")).parse_args([])

        assert args.surface == ["chat", "cowork"]

    def test_explicit_single_value(_):
        args = _build_parser(("code",)).parse_args(["--surface", "vsc"])

        assert args.surface == ["vsc"]

    def test_explicit_combined_values(_):
        args = _build_parser(("code",)).parse_args(
            ["--surface", "chat", "cowork"]
        )

        assert args.surface == ["chat", "cowork"]

    def test_invalid_surface_name_raises(_):
        with pytest.raises(SystemExit):
            _build_parser(("code",)).parse_args(["--surface", "nonexistent"])

    def test_choices_follow_the_registry(_):
        register_render_profile("extra", RenderProfile())

        args = _build_parser(("code",)).parse_args(["-u", "extra"])

        assert args.surface == ["extra"]


class TestEmptyRegistry:

    def test_surface_flag_omitted(_):
        with isolated_render_profiles():
            parser = _build_parser(("code",))

            with pytest.raises(SystemExit):
                parser.parse_args(["--surface", "code"])


@pytest.mark.usefixtures("four_profiles")
class TestResolveSurfaces:

    @staticmethod
    def _resolve(argv):
        parser = ArgumentParser(
            parents=[build_render_profile_parent_parser(default_surface=())]
        )
        return resolve_render_profile(parser.parse_args(argv))

    def test_merges_each_surface_in_order(_):
        profile = TestResolveSurfaces._resolve(
            ["--surface", "chat", "code"]
        )

        assert profile.conditional_sidecars == ("[chat]", "[code]")

    def test_no_surface_leaves_profile_bare(_):
        profile = TestResolveSurfaces._resolve([])

        assert profile.conditional_sidecars == ()
