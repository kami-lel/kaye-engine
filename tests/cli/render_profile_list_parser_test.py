"""
render_profile_list_parser_test.py

Unit Tests (using pytest) for:

_list_render_profile_main, register_render_profile_list_parser
"""

import json
from argparse import ArgumentParser

import pytest

from kaye_engine.cli import render_profile_list_parser
from kaye_engine.prompt.blueprint.render_mode import RenderMode
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.blueprint.render_profile_registry import (
    register_render_profile,
)
from tests.consumer_helper import isolated_render_profiles

_HEADING = "profile\tvariants\tsidecars\tremark"


# auxiliaries  #################################################################
def _build_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    render_profile_list_parser.register_render_profile_list_parser(subparser)
    return root_parser


def _run(argv):
    args = _build_parser().parse_args(argv)
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


@pytest.fixture(autouse=True)
def _fixed_width(monkeypatch):
    monkeypatch.setenv("COLUMNS", "80")


# pytest  ######################################################################
class TestRegister:

    @pytest.mark.parametrize("name", ["render-profile", "rp"])
    def test_registers_names(_, name):
        args = _build_parser().parse_args([name])

        assert args.func is render_profile_list_parser._list_render_profile_main

    @pytest.mark.parametrize(
        "old_flag",
        ["-i", "-I", "-m", "-s", "-v", "-R", "--info", "--no-info", "--remark"],
    )
    def test_rejects_old_flags(_, old_flag):
        with pytest.raises(SystemExit):
            _build_parser().parse_args(["rp", old_flag])

    def test_rejects_positional_argument(_):
        with pytest.raises(SystemExit):
            _build_parser().parse_args(["rp", "zeta"])


@pytest.mark.usefixtures("profiles")
class TestOutput:

    def test_default_prints_heading_and_count_columns_piped_as_names(
        _, capsys
    ):
        _run(["rp"])

        assert capsys.readouterr().out == (
            _HEADING + "\n"
            "alpha\t\t\tfirst one\n"
            "bare\t\t\t\n"
            "zeta\tv1,v2\t[v1],avoid\tlast one\n"
        )

    def test_names_only(_, capsys):
        _run(["rp", "-N"])

        assert capsys.readouterr().out == "alpha\nbare\nzeta\n"

    def test_long_names_only_flag(_, capsys):
        _run(["render-profile", "--names-only"])

        assert capsys.readouterr().out == "alpha\nbare\nzeta\n"

    def test_columns_pick_and_order(_, capsys):
        _run(["rp", "-c", "sparseness,mode"])

        assert capsys.readouterr().out == (
            "profile\tsparseness\tmode\n"
            "alpha\t1\tNORMAL\n"
            "bare\t1\tNORMAL\n"
            "zeta\t3\tNEGATIVE\n"
        )

    @pytest.mark.parametrize(
        ("column", "zeta_cell"),
        [
            ("remark", "last one"),
            ("mode", "NEGATIVE"),
            ("sparseness", "3"),
            ("variants", "v1,v2"),
            ("sidecars", "[v1],avoid"),
        ],
    )
    def test_each_column_is_reachable(_, capsys, column, zeta_cell):
        _run(["rp", "--columns", column])
        lines = capsys.readouterr().out.splitlines()

        assert lines[0] == "profile\t" + column
        assert lines[-1] == "zeta\t" + zeta_cell

    def test_unknown_column_is_rejected(_):
        with pytest.raises(SystemExit):
            _build_parser().parse_args(["rp", "-c", "nope"])

    def test_regex_filters_names(_, capsys):
        _run(["rp", "-r", "^[ab]", "-N"])

        assert capsys.readouterr().out == "alpha\nbare\n"

    def test_json_keeps_lists_whole(_, capsys):
        _run(["rp", "-f", "json", "-r", "zeta"])

        assert json.loads(capsys.readouterr().out) == [
            {
                "profile": "zeta",
                "variants": ["v1", "v2"],
                "sidecars": ["[v1]", "avoid"],
                "remark": "last one",
            }
        ]

    def test_no_variants_prints_empty_cell(_, capsys):
        with isolated_render_profiles():
            register_render_profile("off", RenderProfile(variants=None))
            register_render_profile("none", RenderProfile(variants=()))
            _run(["rp", "-c", "variants"])

        assert capsys.readouterr().out == "profile\tvariants\nnone\t\noff\t\n"


@pytest.mark.usefixtures("profiles")
class TestLong:

    def test_card_folds_echoed_sidecars_into_one_phrase(_, capsys):
        _run(["rp", "-l", "-r", "zeta"])

        assert capsys.readouterr().out == (
            "zeta: last one\n"
            "  mode        NEGATIVE\n"
            "  sparseness  3\n"
            "  variants    (2)\n"
            "    v1   v2\n"
            "  sidecars    (2): the variants in [ ], plus\n"
            "    avoid\n"
        )

    def test_empty_lists_print_zero_counts(_, capsys):
        _run(["rp", "--long", "-r", "^alpha$"])

        assert capsys.readouterr().out == (
            "alpha: first one\n"
            "  mode        NORMAL\n"
            "  sparseness  1\n"
            "  variants    (0)\n"
            "  sidecars    (0)\n"
        )

    def test_columns_narrow_the_card(_, capsys):
        _run(["rp", "-l", "-r", "zeta", "-c", "variants"])

        assert capsys.readouterr().out == (
            "zeta: last one\n  variants  (2)\n    v1   v2\n"
        )

    def test_sidecars_all_echoed_print_the_phrase_alone(_, capsys):
        with isolated_render_profiles():
            register_render_profile(
                "echo",
                RenderProfile(
                    variants=("v1",), conditional_sidecars=("[v1]",)
                ),
            )
            _run(["rp", "-l", "-c", "sidecars"])

        assert capsys.readouterr().out == (
            "echo\n  sidecars  (1): the variants in [ ]\n"
        )

    def test_sidecars_none_echoed_list_every_name(_, capsys):
        with isolated_render_profiles():
            register_render_profile(
                "plain", RenderProfile(conditional_sidecars=("avoid",))
            )
            _run(["rp", "-l", "-c", "sidecars"])

        assert capsys.readouterr().out == (
            "plain\n  sidecars  (1)\n    avoid\n"
        )

    def test_names_only_beats_long(_, capsys):
        _run(["rp", "-l", "-N"])

        assert capsys.readouterr().out == "alpha\nbare\nzeta\n"

    def test_json_beats_long(_, capsys):
        _run(["rp", "-l", "-f", "json", "-r", "bare"])

        assert json.loads(capsys.readouterr().out)[0]["profile"] == "bare"


class TestEmptyRegistry:

    def test_prints_only_the_heading(_, capsys):
        with isolated_render_profiles():
            _run(["rp"])

        assert capsys.readouterr().out == _HEADING + "\n"

    def test_names_only_prints_nothing(_, capsys):
        with isolated_render_profiles():
            _run(["rp", "-N"])

        assert capsys.readouterr().out == ""


class TestBuiltIns:

    def test_names_only_lists_the_eight_built_ins(_, capsys):
        _run(["rp", "-N"])

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
        _run(["rp", "-c", "remark"])

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

    def test_every_built_in_row_has_4_columns(_, capsys):
        _run(["rp"])
        heading, *rows = capsys.readouterr().out.splitlines()

        assert heading == _HEADING
        assert len(rows) == 8
        assert all(row.count("\t") == 3 for row in rows)

    def test_long_card_of_every_built_in_prints(_, capsys):
        _run(["rp", "-l"])
        out = capsys.readouterr().out

        assert out.count("  sparseness  ") == 8
