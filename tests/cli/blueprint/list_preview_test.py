"""
list_preview_test.py

Unit Tests (using pytest) for:

- ``blueprint list`` / ``ls``
- ``blueprint preview`` / ``p``, with ``-D``, ``--preview-line-count``,
  ``--preview-line-width``, ``--show-full-tree``
"""

import json

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

    def test_bare_command_equals_list(_, run):
        bare_exit, bare_out = run([])
        list_exit, list_out = run(["list"])

        assert bare_exit == list_exit == 0
        assert bare_out == list_out

    def test_tty_has_colored_banner_with_count(_, run, monkeypatch):
        monkeypatch.delenv("NO_COLOR", raising=False)

        _exit, out = run(["list"], tty=True)

        first = out.splitlines()[0]
        assert "  blueprints: {}  ".format(len(blueprint_registry)) in first
        assert "\033[96mtest-cli-base\033[0m" in out

    def test_tty_no_color_env_is_banner_and_plain_names(_, run, monkeypatch):
        monkeypatch.setenv("NO_COLOR", "1")

        _exit, out = run(["list"], tty=True)

        assert "\033[" not in out
        assert "test-cli-base" in out.splitlines()

    def test_regex_filters_names(_, run):
        _exit, out = run(["list", "-r", "base$"])

        assert out.splitlines() == ["test-cli-base"]

    def test_json_format(_, run):
        _exit, out = run(["ls", "-f", "json"])

        assert "test-cli-base" in json.loads(out)

    def test_names_registered_blueprints(_, run):
        _exit, out = run(["list"])

        assert "test-cli-base" in out.splitlines()
        assert "test-cli-top" in out.splitlines()


class TestPreview:

    def test_tty_has_banner_with_display_name(_, run):
        _exit, out = run(["preview", "test-cli-base"], tty=True)

        assert "  Display Name  " in out.splitlines()[0]

    def test_no_color_flag_keeps_banner_plain(_, run, monkeypatch):
        monkeypatch.delenv("NO_COLOR", raising=False)

        _exit, colored = run(["preview", "test-cli-base"], tty=True)
        _exit, plain = run(["preview", "test-cli-base", "-C"], tty=True)

        assert "\033[" in colored.splitlines()[0]
        assert "\033[" not in plain.splitlines()[0]
        assert "  Display Name  " in plain.splitlines()[0]

    def test_no_comment_is_long_form_only(_, run):
        _exit, out = run(["preview", "test-cli-base", "--no-comment"])

        assert "<!--" not in out

    def test_piped_has_no_banner(_, run):
        _exit, out = run(["preview", "test-cli-base"])

        assert "-----" not in out.splitlines()[0]

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
        _exit, out = run(["preview", "test-cli-base", "--show-full-tree"])

        assert "[ ] │   └── License" in out

    def test_line_width_flag_is_accepted(_, run):
        exit_code, _out = run(
            ["preview", "test-cli-base", "--preview-line-width", "5"]
        )

        assert exit_code == 0

    @pytest.mark.parametrize("flag", ["-l", "-w", "-t"])
    def test_colliding_short_flags_are_gone(_, run, flag):
        with pytest.raises(SystemExit):
            run(["preview", "test-cli-base", flag])

    def test_line_count_flag_is_accepted(_, run):
        exit_code, _out = run(
            ["preview", "test-cli-base", "--preview-line-count", "1"]
        )

        assert exit_code == 0
