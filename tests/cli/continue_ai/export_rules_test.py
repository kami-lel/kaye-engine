"""
export_rules_test.py

Unit Tests (using pytest) for:

- classify_exportable()

"""

from unittest.mock import MagicMock


from kaye_engine.cli.continue_ai.export_rules import (
    classify_exportable,
)
from kaye_engine.cli.exportable_abbr import ExportableAbbr
from kaye_engine.prompt.blueprint import BlueprintRegistry


def _registry(name, **kwargs):
    blueprint = MagicMock()
    blueprint.sidecars.description_and_when_to_use = "d"
    blueprint.sidecars.globs = []
    blueprint.render_prompt.return_value = "body of " + name
    return BlueprintRegistry(
        canonical_name=name,
        display_name="Display " + name,
        blueprint=blueprint,
        **kwargs,
    )


# pytest  ######################################################################
class TestClassifyExportable:

    def test_always_apply_beats_llm_invokable_false(_):
        reg = _registry("x", always_apply=True, llm_invokable=False)

        assert classify_exportable(reg) == "rule"

    def test_always_apply_beats_not_user_invokable(_):
        reg = _registry(
            "x",
            always_apply=True,
            llm_invokable=False,
            is_user_invokable=False,
        )

        assert classify_exportable(reg) == "rule"

    def test_llm_invokable_is_rule(_):
        assert classify_exportable(_registry("x")) == "rule"

    def test_user_invokable_only_is_prompt(_):
        reg = _registry("x", llm_invokable=False)

        assert classify_exportable(reg) == "prompt"

    def test_neither_invokable_is_skipped(_):
        reg = _registry("x", llm_invokable=False, is_user_invokable=False)

        assert classify_exportable(reg) is None

    def test_abbr_group_is_rule(_):
        group = ExportableAbbr(canonical_name="a", display_name="A")

        assert classify_exportable(group) == "rule"
