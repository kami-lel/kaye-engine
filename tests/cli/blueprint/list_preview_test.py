"""
list_preview_test.py

Unit Tests (using pytest) for:

- ``blueprint list`` / ``ls``
- ``blueprint preview`` / ``p``, with ``-D``, ``-l``, ``-w``, ``-t``
"""

import pytest

from kaye_engine.prompt.blueprint import blueprint_registry

TREE = """    ○
[x] └── Project
[x]     ├── Install
[ ]     └── License"""


class TestList:

    @pytest.mark.parametrize("verb", ["list", "ls"])
    def test_prints_sorted_names_one_per_line(_, run, verb):
        exit_code, out = run([verb])

        assert exit_code == 0
        assert out.splitlines() == sorted(blueprint_registry)

    def test_names_registered_blueprints(_, run):
        _exit, out = run(["list"])

        assert "test-cli-base" in out.splitlines()
        assert "test-cli-top" in out.splitlines()


class TestPreview:

    @pytest.mark.parametrize("verb", ["preview", "p"])
    def test_named_blueprint(_, run, verb):
        exit_code, out = run([verb, "test-cli-base"])

        assert exit_code == 0
        assert "[x] └── Project" in out
        assert "[x]     └── Install" in out

    def test_dependencies_included_by_default(_, run):
        _exit, out = run(["preview", "test-cli-top"])

        assert "[x]     ├── Install" in out
        assert "[x]     └── License" in out

    @pytest.mark.parametrize("flag", ["-D", "--no-dependencies"])
    def test_no_dependencies_flag_shows_own_nodes(_, run, flag):
        _exit, out = run(["preview", "test-cli-top", flag])

        assert "[x]     └── License" in out
        assert "Install" not in out

    def test_stdin_tree(_, run):
        exit_code, out = run(["preview"], stdin=TREE)

        assert exit_code == 0
        assert "[x] └── Project" in out
        assert "[x]     └── Install" in out
        assert "License" not in out

    def test_stdin_json(_, run):
        json_text = (
            '{"schema": 1, "nodes": [["Project"], ["Project", "Install"]]}'
        )

        exit_code, out = run(["preview"], stdin=json_text)

        assert exit_code == 0
        assert "[x] └── Project" in out

    def test_unknown_name_exits_1(_, run):
        exit_code, out = run(["preview", "no-such-blueprint"])

        assert exit_code == 1
        assert out == ""

    def test_malformed_stdin_exits_1(_, run):
        exit_code, _out = run(["preview"], stdin="{nope")

        assert exit_code == 1

    def test_full_tree_flag_shows_unchecked(_, run):
        _exit, out = run(["preview", "test-cli-base", "-t"])

        assert "[ ] │   └── License" in out

    def test_line_width_flag_is_accepted(_, run):
        exit_code, _out = run(["preview", "test-cli-base", "-w", "5"])

        assert exit_code == 0

    def test_line_count_flag_is_accepted(_, run):
        exit_code, _out = run(["preview", "test-cli-base", "-l", "1"])

        assert exit_code == 0
