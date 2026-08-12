"""
tests/cli/claude/surface_parser_test.py

Unit Tests (using pytest) for:

build_surface_parent_parser
"""

from argparse import ArgumentParser

import pytest

from kaye_engine.cli.claude.surface_parser import build_surface_parent_parser


def _build_parser(default):
    parent = build_surface_parent_parser(default)
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
