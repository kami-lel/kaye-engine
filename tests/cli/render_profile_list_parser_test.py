"""
render_profile_list_parser_test.py

Unit Tests (using pytest) for:

_list_render_profile_main, register_render_profile_list_parser
"""

from argparse import ArgumentParser

import pytest

from kaye_engine.cli import render_profile_list_parser
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.blueprint.render_profile_registry import (
    register_render_profile,
)
from tests.consumer_helper import isolated_render_profiles


# auxiliaries  ##################################################################
def _run(argv):
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    render_profile_list_parser.register_render_profile_list_parser(subparser)
    args = root_parser.parse_args(argv)
    args.func(args)


@pytest.fixture(name="profiles")
def fixture_profiles():
    with isolated_render_profiles():
        register_render_profile("zeta", RenderProfile(), "last one")
        register_render_profile("alpha", RenderProfile(), "first one")
        register_render_profile("bare", RenderProfile())
        yield


# pytest  ######################################################################
class TestRegister:

    @pytest.mark.parametrize("name", ["render-profile", "rp"])
    def test_registers_names(_, name):
        root_parser = ArgumentParser()
        subparser = root_parser.add_subparsers()
        render_profile_list_parser.register_render_profile_list_parser(
            subparser
        )

        args = root_parser.parse_args([name])

        assert args.func is render_profile_list_parser._list_render_profile_main
        assert args.show_remark is True


@pytest.mark.usefixtures("profiles")
class TestOutput:

    def test_default_prints_remarks_tab_separated(_, capsys):
        _run(["rp"])

        assert capsys.readouterr().out == (
            "alpha:\tfirst one\nbare\nzeta:\tlast one\n"
        )

    def test_r_matches_default(_, capsys):
        _run(["rp", "-r"])

        assert capsys.readouterr().out == (
            "alpha:\tfirst one\nbare\nzeta:\tlast one\n"
        )

    def test_capital_r_prints_names_only(_, capsys):
        _run(["rp", "-R"])

        assert capsys.readouterr().out == "alpha\nbare\nzeta\n"

    def test_long_flags(_, capsys):
        _run(["render-profile", "--no-remark"])

        assert capsys.readouterr().out == "alpha\nbare\nzeta\n"

    def test_last_flag_wins(_, capsys):
        _run(["rp", "-r", "-R"])
        names_only = capsys.readouterr().out
        _run(["rp", "-R", "-r"])
        with_remark = capsys.readouterr().out

        assert names_only == "alpha\nbare\nzeta\n"
        assert with_remark == "alpha:\tfirst one\nbare\nzeta:\tlast one\n"


class TestEmptyRegistry:

    def test_prints_nothing(_, capsys):
        with isolated_render_profiles():
            _run(["rp"])

        assert capsys.readouterr().out == ""


class TestBuiltIns:

    def test_default_output_lists_the_eight_built_ins(_, capsys):
        _run(["rp"])

        assert capsys.readouterr().out == (
            "chat:\tAnthropic Claude chat app on web and desktop\n"
            "code:\tAnthropic Claude Code in the terminal\n"
            "comfy:\tComfy Org ComfyUI image prompts\n"
            "continue:\tContinue.dev rules\n"
            "cowork:\tAnthropic Claude Cowork desktop agent\n"
            "hermes:\tHermes Agents\n"
            "ioschat:\tAnthropic Claude chat app on Apple iOS\n"
            "vsc:\tAnthropic Claude Code extension for Microsoft Visual"
            " Studio Code\n"
        )
