"""
render_profile_list_parser_test.py

Unit Tests (using pytest) for:

_list_render_profile_main, register_render_profile_list_parser
"""

from argparse import ArgumentParser

import pytest

from kaye_engine.cli import render_profile_list_parser
from kaye_engine.prompt.blueprint.render_mode import RenderMode
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.blueprint.render_profile_registry import (
    register_render_profile,
)
from tests.consumer_helper import isolated_render_profiles

_HEADING = "profile\tremark\tmode\tsparseness\tvariants\tsidecars"


# auxiliaries  #################################################################
def _run(argv):
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    render_profile_list_parser.register_render_profile_list_parser(subparser)
    args = root_parser.parse_args(argv)
    args.func(args)


@pytest.fixture(name="profiles")
def fixture_profiles():
    with isolated_render_profiles():
        register_render_profile(
            "zeta",
            RenderProfile(
                variants=("v1", "v2"),
                conditional_sidecars=("[v1]", "avoid"),
                sparseness=3,
                mode=RenderMode.NEGATIVE,
            ),
            "last one",
        )
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

    def test_rejects_old_no_remark_flags(_):
        root_parser = ArgumentParser()
        subparser = root_parser.add_subparsers()
        render_profile_list_parser.register_render_profile_list_parser(
            subparser
        )

        for old_flag in ("-R", "--no-remark"):
            with pytest.raises(SystemExit):
                root_parser.parse_args(["rp", old_flag])


@pytest.mark.usefixtures("profiles")
class TestOutput:

    def test_default_prints_heading_and_every_column(_, capsys):
        _run(["rp"])

        assert capsys.readouterr().out == (
            _HEADING + "\n"
            "alpha\tfirst one\tNORMAL\t1\t\t\n"
            "bare\t\tNORMAL\t1\t\t\n"
            "zeta\tlast one\tNEGATIVE\t3\tv1,v2\t[v1],avoid\n"
        )

    def test_info_matches_default(_, capsys):
        _run(["rp", "-i"])
        with_info = capsys.readouterr().out
        _run(["rp"])

        assert with_info == capsys.readouterr().out

    def test_no_info_prints_names_only_without_heading(_, capsys):
        _run(["rp", "-I"])

        assert capsys.readouterr().out == "alpha\nbare\nzeta\n"

    def test_long_flag(_, capsys):
        _run(["render-profile", "--no-info"])

        assert capsys.readouterr().out == "alpha\nbare\nzeta\n"

    def test_remark_only(_, capsys):
        _run(["rp", "-r"])

        assert capsys.readouterr().out == (
            "profile\tremark\nalpha\tfirst one\nbare\t\nzeta\tlast one\n"
        )

    def test_each_column_flag_selects_its_column(_, capsys):
        for flag, heading, zeta_cell in (
            ("-m", "mode", "NEGATIVE"),
            ("-s", "sparseness", "3"),
            ("-v", "variants", "v1,v2"),
            ("-c", "sidecars", "[v1],avoid"),
        ):
            _run(["rp", flag])
            lines = capsys.readouterr().out.splitlines()

            assert lines[0] == "profile\t" + heading
            assert lines[-1] == "zeta\t" + zeta_cell

    def test_columns_keep_table_order_not_flag_order(_, capsys):
        _run(["rp", "-c", "-m"])

        assert capsys.readouterr().out.splitlines()[0] == (
            "profile\tmode\tsidecars"
        )

    def test_last_flag_wins(_, capsys):
        _run(["rp", "-r", "-I"])
        nothing = capsys.readouterr().out
        _run(["rp", "-I", "-r"])
        remark_only = capsys.readouterr().out

        assert nothing == "alpha\nbare\nzeta\n"
        assert remark_only.splitlines()[0] == "profile\tremark"

    def test_no_variants_prints_empty_cell(_, capsys):
        with isolated_render_profiles():
            register_render_profile("off", RenderProfile(variants=None))
            register_render_profile("none", RenderProfile(variants=()))
            _run(["rp", "-v"])

        assert capsys.readouterr().out == "profile\tvariants\nnone\t\noff\t\n"


class TestEmptyRegistry:

    def test_prints_only_the_heading(_, capsys):
        with isolated_render_profiles():
            _run(["rp"])

        assert capsys.readouterr().out == _HEADING + "\n"

    def test_no_info_prints_nothing(_, capsys):
        with isolated_render_profiles():
            _run(["rp", "-I"])

        assert capsys.readouterr().out == ""


class TestBuiltIns:

    def test_no_info_lists_the_eight_built_ins(_, capsys):
        _run(["rp", "-I"])

        assert capsys.readouterr().out.splitlines() == [
            "chat",
            "code",
            "comfy",
            "continue",
            "cowork",
            "hermes",
            "ioschat",
            "vsc",
        ]

    def test_remark_column_lists_the_built_in_remarks(_, capsys):
        _run(["rp", "-r"])

        assert capsys.readouterr().out == (
            "profile\tremark\n"
            "chat\tAnthropic Claude chat app on web and desktop\n"
            "code\tAnthropic Claude Code in the terminal\n"
            "comfy\tComfy Org ComfyUI image prompts\n"
            "continue\tContinue.dev rules\n"
            "cowork\tAnthropic Claude Cowork desktop agent\n"
            "hermes\tHermes Agents\n"
            "ioschat\tAnthropic Claude chat app on Apple iOS\n"
            "vsc\tAnthropic Claude Code extension for Microsoft Visual"
            " Studio Code\n"
        )

    def test_every_built_in_row_has_6_columns(_, capsys):
        _run(["rp"])
        heading, *rows = capsys.readouterr().out.splitlines()

        assert heading == _HEADING
        assert len(rows) == 8
        assert all(row.count("\t") == 5 for row in rows)
