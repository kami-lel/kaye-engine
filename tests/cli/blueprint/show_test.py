"""
show_test.py

Unit Tests (using pytest) for:

- ``blueprint show`` / ``s``: the summary, and the field flags
  ``-d -w -g -p`` with their long forms and the long-only
  ``--description-node``, ``--when-to-use-node``, mutually exclusive
"""

import pytest

from kaye_engine.cli.blueprint.aux_output import SHOW_FIELD_FXS
from kaye_engine.prompt.blueprint import Blueprint, BlueprintMeta

TREE = """    ○
[x] └── Project
[x]     ├── Install
[ ]     └── License"""


class TestSummary:

    @pytest.mark.parametrize("verb", ["show", "s"])
    def test_named_blueprint(_, run, verb):
        exit_code, out = run([verb, "test-cli-top"])

        assert exit_code == 0
        assert "nodes: 1" in out
        assert "dependencies: test-cli-base" in out

    def test_stdin_tree(_, run):
        exit_code, out = run(["show"], stdin=TREE)

        assert exit_code == 0
        assert "nodes: 2" in out
        assert "dependencies: -" in out

    def test_stdin_json(_, run):
        text = '{"schema": 1, "nodes": [["Project"]], "dependencies": ["x"]}'

        exit_code, out = run(["show"], stdin=text)

        assert exit_code == 0
        assert "nodes: 1" in out
        assert "dependencies: x" in out

    def test_unknown_name_exits_1(_, run):
        exit_code, out = run(["show", "no-such-blueprint"])

        assert exit_code == 1
        assert out == ""


class TestFields:

    @pytest.mark.parametrize("flag", ["-p", "--dependencies"])
    def test_dependencies_one_per_line(_, run, registered, flag):
        registered(
            "test-cli-two-deps",
            Blueprint(dependencies=("test-cli-base", "test-cli-top")),
        )

        exit_code, out = run(["show", "test-cli-two-deps", flag])

        assert exit_code == 0
        assert out == "test-cli-base\ntest-cli-top\n"

    @pytest.mark.parametrize("flag", ["-n", "--display-name"])
    def test_display_name(_, run, registered, flag):
        registered(
            "test-cli-named",
            Blueprint(meta=BlueprintMeta(display_name="Nice Name")),
        )

        exit_code, out = run(["show", "test-cli-named", flag])

        assert exit_code == 0
        assert out == "Nice Name\n"

    def test_display_name_empty_when_unnamed(_, run):
        exit_code, out = run(["show", "test-cli-base", "-n"])

        assert exit_code == 0
        assert out == "\n"

    def test_summary_shows_display_name_first(_, run, registered):
        registered(
            "test-cli-named-2",
            Blueprint(meta=BlueprintMeta(display_name="Nice Name")),
        )

        exit_code, out = run(["show", "test-cli-named-2"])

        assert exit_code == 0
        assert out.startswith("display name: Nice Name\n")

    @pytest.mark.parametrize("flag", ["-d", "--description"])
    def test_description(_, run, registered, flag):
        registered(
            "test-cli-described",
            Blueprint(meta=BlueprintMeta(description="what it is")),
        )

        exit_code, out = run(["show", "test-cli-described", flag])

        assert exit_code == 0
        assert out == "what it is\n"

    @pytest.mark.parametrize("flag", ["-w", "--when-to-use"])
    def test_when_to_use_empty_without_node(_, run, flag):
        exit_code, out = run(["show", "test-cli-base", flag])

        assert exit_code == 0
        assert out == "\n"

    @pytest.mark.parametrize("flag", ["-g", "--globs"])
    def test_globs_empty_without_node(_, run, flag):
        exit_code, out = run(["show", "test-cli-base", flag])

        assert exit_code == 0
        assert out == "\n"

    def test_field_from_stdin(_, run):
        text = '{"schema": 1, "dependencies": ["test-cli-base"]}'

        exit_code, out = run(["show", "--dependencies"], stdin=text)

        assert exit_code == 0
        assert out == "test-cli-base\n"

    def test_every_field_flag_maps_to_an_api_function(_):
        assert set(SHOW_FIELD_FXS) == {
            "display-name",
            "description",
            "description-node",
            "when-to-use",
            "when-to-use-node",
            "globs",
            "dependencies",
        }

    @pytest.mark.parametrize(
        "flag", ["--description-node", "--when-to-use-node"]
    )
    def test_node_path_dash_when_unset(_, run, flag):
        exit_code, out = run(["show", "test-cli-base", flag])

        assert exit_code == 0
        assert out == "-\n"


    @pytest.mark.parametrize(
        "flags",
        [
            ["-d", "-w"],
            ["-g", "-p"],
            ["--description", "--globs"],
            ["--description-node", "--when-to-use-node"],
        ],
    )
    def test_field_flags_are_mutually_exclusive(_, run, flags):
        with pytest.raises(SystemExit) as info:
            run(["show", "test-cli-base", *flags])

        assert info.value.code == 2

    def test_unknown_name_exits_1(_, run):
        exit_code, _out = run(["show", "no-such-blueprint", "-d"])

        assert exit_code == 1
