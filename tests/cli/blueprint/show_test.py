"""
show_test.py

Unit Tests (using pytest) for:

- ``blueprint show`` / ``s``: the summary, and the field flags
  ``-a -d -D -w -W -n -t -g -p`` with their long forms, mutually
  exclusive
"""

import kamilog
import pytest

from kaye_engine.cli.blueprint.aux_output import SHOW_FIELD_FXS
from kaye_engine.prompt.blueprint import Blueprint, BlueprintMeta

TREE = """    ○
[x] └── Project
[x]     ├── Install
[ ]     └── License"""


def _field(label, value):
    return kamilog.gen_comment_banner_centered(label, 5) + "\n" + value


class TestSummary:

    @pytest.mark.parametrize("verb", ["show", "s"])
    def test_named_blueprint(_, run, verb):
        exit_code, out = run([verb, "test-cli-top"])

        assert exit_code == 0
        assert "  nodes: 1  " in out
        assert _field("dependencies", "test-cli-base") in out

    def test_stdin_tree(_, run):
        exit_code, out = run(["show"], stdin=TREE)

        assert exit_code == 0
        assert "  nodes: 2  " in out
        assert "dependencies" not in out

    def test_stdin_json(_, run):
        text = '{"schema": 1, "nodes": [["Project"]], "dependencies": ["x"]}'

        exit_code, out = run(["show"], stdin=text)

        assert exit_code == 0
        assert "  nodes: 1  " in out
        assert _field("dependencies", "x") in out

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

    @pytest.mark.parametrize("flag", ["-a", "--display-name"])
    def test_display_name(_, run, registered, flag):
        registered(
            "test-cli-named",
            Blueprint(meta=BlueprintMeta(display_name="Nice Name")),
        )

        exit_code, out = run(["show", "test-cli-named", flag])

        assert exit_code == 0
        assert out == "Nice Name\n"

    def test_display_name_empty_when_unnamed(_, run):
        exit_code, out = run(["show", "test-cli-base", "-a"])

        assert exit_code == 0
        assert out == "\n"

    def test_summary_shows_display_name_first(_, run, registered):
        registered(
            "test-cli-named-2",
            Blueprint(meta=BlueprintMeta(display_name="Nice Name")),
        )

        exit_code, out = run(["show", "test-cli-named-2"])

        assert exit_code == 0
        assert out.startswith(_field("display name", "Nice Name") + "\n")

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

    @pytest.mark.parametrize(
        "flag", ["-D", "--description-node", "-W", "--when-to-use-node"]
    )
    def test_node_empty_when_unset(_, run, flag):
        exit_code, out = run(["show", "test-cli-base", flag])

        assert exit_code == 0
        assert out == "\n"

    @pytest.mark.parametrize(
        ("flag", "field"),
        [
            ("-D", "description_node"),
            ("--description-node", "description_node"),
            ("-W", "when_to_use_node"),
            ("--when-to-use-node", "when_to_use_node"),
        ],
    )
    def test_node_shows_lineage(_, run, registered, flag, field):
        registered(
            "test-cli-lineage",
            Blueprint(meta=BlueprintMeta(**{field: ("A", "B")})),
        )

        exit_code, out = run(["show", "test-cli-lineage", flag])

        assert exit_code == 0
        assert out == "A # B\n"

    @pytest.mark.parametrize("flag", ["-n", "--nodes"])
    def test_nodes_one_lineage_per_line(_, run, flag):
        exit_code, out = run(["show", "test-cli-base", flag])

        assert exit_code == 0
        assert out == "Project\nProject # Install\n"

    @pytest.mark.parametrize("flag", ["-t", "--subtrees"])
    def test_subtrees_one_lineage_per_line(_, run, registered, flag):
        registered(
            "test-cli-subtrees",
            Blueprint(
                subtrees=frozenset({("Project", "License"), ("Project",)})
            ),
        )

        exit_code, out = run(["show", "test-cli-subtrees", flag])

        assert exit_code == 0
        assert out == "Project\nProject # License\n"

    def test_subtrees_empty_when_none(_, run):
        exit_code, out = run(["show", "test-cli-base", "--subtrees"])

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
            "nodes",
            "subtrees",
            "globs",
            "dependencies",
        }


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
