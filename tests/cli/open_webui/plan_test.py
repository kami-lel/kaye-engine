"""
plan_test.py

Unit Tests (using pytest) for:

plan_skill_sync
"""

from kaye_engine.cli.open_webui.plan import plan_skill_sync


# auxiliaries  #################################################################
def _build_form(skill_id="a", content="body"):
    return {
        "id": skill_id,
        "name": skill_id.upper(),
        "description": "d",
        "content": content,
        "meta": {"tags": []},
        "is_active": True,
    }


# pytest  ######################################################################
class TestPlanSkillSync:

    def test_absent_id_is_created(_):
        plan = plan_skill_sync([_build_form("a")], [])

        assert plan.create == [_build_form("a")]
        assert not plan.update and not plan.skip and not plan.prune

    def test_changed_field_is_updated(_):
        remote = _build_form("a", content="old")
        plan = plan_skill_sync([_build_form("a")], [remote])

        assert plan.update == [_build_form("a")]
        assert not plan.create and not plan.skip

    def test_identical_record_is_skipped(_):
        plan = plan_skill_sync([_build_form("a")], [_build_form("a")])

        assert plan.skip == ["a"]
        assert not plan.create and not plan.update

    def test_server_owned_fields_do_not_trigger_update(_):
        remote = dict(_build_form("a"), updated_at=1, user_id="u")
        plan = plan_skill_sync([_build_form("a")], [remote])

        assert plan.skip == ["a"]

    def test_remote_only_id_is_pruned(_):
        plan = plan_skill_sync([_build_form("a")], [_build_form("z")])

        assert plan.prune == ["z"]
        assert plan.create == [_build_form("a")]

    def test_empty_inputs_yield_empty_plan(_):
        plan = plan_skill_sync([], [])

        assert plan.create == [] and plan.update == []
        assert plan.skip == [] and plan.prune == []
