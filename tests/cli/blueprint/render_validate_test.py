"""
render_validate_test.py

Unit Tests (using pytest) for:

- ``blueprint render`` / ``r``, with ``-D`` and the render profile flags
- ``blueprint validate`` / ``v``
- ``generate`` no longer existing
"""

import pytest

from kaye_engine.prompt.blueprint import Blueprint
from kaye_engine.prompt.blueprint.render_profile import RenderProfile

TREE = """    ○
[x] └── Project
[x]     ├── Install
[ ]     └── License"""


class TestRender:

    @pytest.mark.parametrize("verb", ["render", "r"])
    def test_named_blueprint(_, run, verb):
        exit_code, out = run([verb, "test-cli-base", "-C"])

        assert exit_code == 0
        assert "Overview text." in out
        assert "Clone it." in out
        assert "MIT." not in out

    def test_dependencies_included_by_default(_, run):
        _exit, out = run(["render", "test-cli-top", "-C"])

        assert "Clone it." in out
        assert "MIT." in out

    @pytest.mark.parametrize("flag", ["-D", "--no-dependencies"])
    def test_no_dependencies_flag_renders_own_nodes(_, run, flag):
        _exit, out = run(["render", "test-cli-top", "-C", flag])

        assert "MIT." in out
        assert "Clone it." not in out

    def test_comment_names_the_registry_entry(_, run):
        _exit, out = run(["render", "test-cli-base"])

        assert "blueprint: Display Name" in out

    def test_no_comment_flag(_, run):
        _exit, out = run(["render", "test-cli-base", "-C"])

        assert "<!--" not in out

    def test_stdin_tree(_, run):
        exit_code, out = run(["render", "-C"], stdin=TREE)

        assert exit_code == 0
        assert "Clone it." in out
        assert "MIT." not in out

    def test_stdin_comment_shows_stdin_name(_, run):
        _exit, out = run(["render"], stdin=TREE)

        assert "blueprint: <stdin>" in out

    def test_unknown_name_exits_1(_, run):
        exit_code, out = run(["render", "no-such-blueprint"])

        assert exit_code == 1
        assert out == ""

    def test_registry_render_profile_is_kept(_, run, registered):
        registered(
            "test-cli-profiled",
            Blueprint(nodes=frozenset({("Project",), ("Project", "Install")})),
            render_profile=RenderProfile(conditional_sidecars=("note",)),
        )

        _exit, plain = run(["render", "test-cli-base", "-C"])
        _exit, profiled = run(["render", "test-cli-profiled", "-C"])

        assert "Noted text." not in plain
        assert "Noted text." in profiled

    def test_registry_profile_is_kept_with_no_dependencies(_, run, registered):
        registered(
            "test-cli-profiled-nd",
            Blueprint(nodes=frozenset({("Project",), ("Project", "Install")})),
            render_profile=RenderProfile(conditional_sidecars=("note",)),
        )

        _exit, plain = run(["render", "test-cli-base", "-C", "-D"])
        _exit, profiled = run(["render", "test-cli-profiled-nd", "-C", "-D"])

        assert "Noted text." not in plain
        assert "Noted text." in profiled

    def test_generate_is_gone(_, run):
        with pytest.raises(SystemExit):
            run(["generate", "test-cli-base"])


class TestValidate:

    @pytest.mark.parametrize("verb", ["validate", "v"])
    def test_registered_blueprint_passes(_, run, verb):
        exit_code, out = run([verb, "test-cli-top"])

        assert exit_code == 0
        assert out == ""

    def test_stdin_tree_passes(_, run):
        exit_code, _out = run(["validate"], stdin=TREE)

        assert exit_code == 0

    def test_stdin_json_with_unknown_dependency_fails(_, run):
        text = '{"schema": 1, "dependencies": ["no-such-blueprint"]}'

        exit_code, _out = run(["validate"], stdin=text)

        assert exit_code == 1

    def test_stdin_json_with_unknown_path_fails(_, run):
        text = '{"schema": 1, "nodes": [["Project", "Nope"]]}'

        exit_code, _out = run(["validate"], stdin=text)

        assert exit_code == 1

    def test_unknown_name_fails(_, run):
        exit_code, _out = run(["validate", "no-such-blueprint"])

        assert exit_code == 1

    def test_malformed_stdin_fails(_, run):
        exit_code, _out = run(["validate"], stdin="{nope")

        assert exit_code == 1
