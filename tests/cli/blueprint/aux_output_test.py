"""
aux_output_test.py

Unit Tests (using pytest) for:

- pick_preview_fx(), pick_render_fx(), pick_show_fx(), SHOW_FIELD_FXS
- fmt_ls(), fmt_summary(), fmt_show_result()
- emit_str(), run_cmd()
"""

import pytest

from kaye_engine.cli.blueprint.aux_output import (
    SHOW_FIELD_FXS,
    emit_str,
    fmt_ls,
    fmt_show_result,
    fmt_summary,
    pick_preview_fx,
    pick_render_fx,
    pick_show_fx,
    run_cmd,
    run_cmd_and_exit,
)
from kaye_engine.prompt.blueprint import (
    Blueprint,
    BlueprintMeta,
    BlueprintSummary,
    preview_blueprint,
    preview_blueprint_without_dependencies,
    render_prompt,
    render_prompt_without_dependencies,
    show_blueprint,
    show_dependencies,
    show_description,
    show_globs,
    show_when_to_use,
)


class TestPick:

    def test_preview(_):
        assert pick_preview_fx(False) is preview_blueprint
        assert pick_preview_fx(True) is preview_blueprint_without_dependencies

    def test_render(_):
        assert pick_render_fx(False) is render_prompt
        assert pick_render_fx(True) is render_prompt_without_dependencies

    def test_show_without_field_is_the_summary(_):
        assert pick_show_fx(None) is show_blueprint

    def test_show_field_map(_):
        assert SHOW_FIELD_FXS == {
            "description": show_description,
            "when-to-use": show_when_to_use,
            "globs": show_globs,
            "dependencies": show_dependencies,
        }

    @pytest.mark.parametrize("field", sorted(SHOW_FIELD_FXS))
    def test_show_field(_, field):
        assert pick_show_fx(field) is SHOW_FIELD_FXS[field]

    def test_show_unknown_field_raises(_):
        with pytest.raises(KeyError):
            pick_show_fx("nope")


class TestFormat:

    def test_ls_one_per_line(_):
        assert fmt_ls(["a", "b"]) == "a\nb"

    def test_ls_empty(_):
        assert fmt_ls([]) == ""

    def test_summary_of_empty_blueprint(_):
        out = fmt_summary(show_blueprint(Blueprint()))

        assert out == (
            "description: -\n"
            "description-node: -\n"
            "when-to-use-node: -\n"
            "globs-node: -\n"
            "nodes: 0\n"
            "subtrees: 0\n"
            "dependencies: -"
        )

    def test_summary_of_filled_blueprint(_):
        bp = Blueprint(
            meta=BlueprintMeta(
                description="d", description_node=("A", "{description}")
            ),
            nodes=frozenset({("A",)}),
            dependencies=("x", "y"),
        )

        out = fmt_summary(show_blueprint(bp))

        assert "description: d" in out
        assert "description-node: A > {description}" in out
        assert "nodes: 1" in out
        assert out.endswith("dependencies: x, y")

    def test_show_result_by_type(_):
        summary = show_blueprint(Blueprint())

        assert fmt_show_result("text") == "text"
        assert fmt_show_result(("a", "b")) == "a\nb"
        assert fmt_show_result(["a"]) == "a"
        assert fmt_show_result(summary) == fmt_summary(summary)
        assert isinstance(summary, BlueprintSummary)


class TestEmit:

    def test_prints_to_stdout(_, capsys):
        emit_str("hello")

        assert capsys.readouterr().out == "hello\n"


class TestRunCmd:

    def test_success_is_0(_):
        calls = []

        assert run_cmd(calls.append, "args") == 0
        assert calls == ["args"]

    @pytest.mark.parametrize(
        "err", [ValueError("bad"), KeyError("bad"), FileNotFoundError("bad")]
    )
    def test_api_error_is_1(_, err):
        def handler(_args):
            raise err

        assert run_cmd(handler, None) == 1

    def test_error_text_is_logged(_, caplog):
        def handler(_args):
            raise ValueError("the reason")

        with caplog.at_level("CRITICAL"):
            run_cmd(handler, None)

        assert "the reason" in caplog.text

    def test_other_errors_propagate(_):
        def handler(_args):
            raise RuntimeError("bug")

        with pytest.raises(RuntimeError):
            run_cmd(handler, None)


class TestRunCmdAndExit:

    def test_success_returns_normally(_):
        assert run_cmd_and_exit(lambda _args: None, None) is None

    def test_failure_exits_1(_):
        def handler(_args):
            raise ValueError("bad")

        with pytest.raises(SystemExit) as info:
            run_cmd_and_exit(handler, None)

        assert info.value.code == 1
