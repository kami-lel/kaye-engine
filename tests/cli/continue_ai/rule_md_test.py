"""
rule_md_test.py

Unit Tests (using pytest) for:

ContinueRule
"""

import yaml

from kaye_engine.cli.continue_ai.rule_md import ContinueRule


def _split(text):
    _, front, body = text.split("---\n", 2)
    return yaml.safe_load(front), body


# pytest  ######################################################################
class TestRender:

    def test_minimal(_):
        opt = ContinueRule(name="x", body="hi").render()

        front, body = _split(opt)
        assert front == {"name": "x", "alwaysApply": False}
        assert body == "\nhi"

    def test_all_fields(_):
        rule = ContinueRule(
            name="x",
            description="d",
            globs=["**/*.py"],
            always_apply=True,
            invokable=True,
            body="b",
        )

        front, _body = _split(rule.render())

        assert front == {
            "name": "x",
            "description": "d",
            "alwaysApply": True,
            "invokable": True,
            "globs": ["**/*.py"],
        }

    def test_empty_optionals_omitted(_):
        rule = ContinueRule(name="x", description="", globs=[])

        front, _body = _split(rule.render())

        assert "description" not in front
        assert "globs" not in front
        assert "invokable" not in front


class TestWrite:

    def test_writes_rendered_text(_, tmp_path):
        rule = ContinueRule(name="x", body="hi")
        path = tmp_path / "x.md"

        rule.write(path)

        assert path.read_text(encoding="utf-8") == rule.render()
