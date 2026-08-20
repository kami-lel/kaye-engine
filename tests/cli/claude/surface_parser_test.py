"""
tests/cli/claude/surface_parser_test.py

Unit Tests (using pytest) for:

build_surface_parent_parser
"""

from argparse import ArgumentParser

import pytest

from kaye_engine.cli.claude.surface_parser import build_surface_parent_parser
from kaye_engine.prompt.blueprint.render_profile import RenderProfile


_SURFACE_PROFILES = {
    "chat": RenderProfile(),
    "cowork": RenderProfile(),
    "code": RenderProfile(),
    "vsc": RenderProfile(),
}


def _build_parser(default, *, surface_profiles=_SURFACE_PROFILES):
    parent = build_surface_parent_parser(
        default, surface_profiles=surface_profiles
    )
    root_parser = ArgumentParser(parents=[parent])
    return root_parser


# Pytest unit tests  ###########################################################
class TestSurfaceFlag:

    def test_default_applied_when_omitted(_):
        parser = _build_parser(("chat", "cowork"))
        args = parser.parse_args([])

        assert args.surface == ["chat", "cowork"]

    def test_explicit_single_value(_):
        parser = _build_parser(("code",))
        args = parser.parse_args(["--surface", "vsc"])

        assert args.surface == ["vsc"]

    def test_explicit_combined_values(_):
        parser = _build_parser(("code",))
        args = parser.parse_args(["--surface", "chat", "cowork"])

        assert args.surface == ["chat", "cowork"]

    def test_invalid_surface_name_raises(_):
        parser = _build_parser(("code",))

        with pytest.raises(SystemExit):
            parser.parse_args(["--surface", "nonexistent"])


class TestSurfaceProfilesUnset:

    def test_surface_flag_omitted_when_none(_):
        parser = _build_parser(("code",), surface_profiles=None)

        with pytest.raises(SystemExit):
            parser.parse_args(["--surface", "code"])

    def test_surface_flag_omitted_when_empty(_):
        parser = _build_parser(("code",), surface_profiles={})

        with pytest.raises(SystemExit):
            parser.parse_args(["--surface", "code"])
