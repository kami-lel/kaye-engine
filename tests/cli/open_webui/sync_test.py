"""
sync_test.py

Unit Tests (using pytest) for:

sync_skills
"""

import logging
from unittest.mock import patch

import pytest

from kaye_engine.cli.open_webui import sync
from kaye_engine.cli.open_webui.client import OpenWebUIError
from kaye_engine.exportable import Exportable


# auxiliaries  #################################################################
class _FakeExportable(Exportable):

    def content(self, **_render_kwargs):
        return "content of " + self.canonical_name

    def merge(self, other):
        raise NotImplementedError


class _FakeClient:

    def __init__(self, remote=(), failing_ids=()):
        self.remote = list(remote)
        self.failing_ids = set(failing_ids)
        self.calls = []

    def export_skills(self):
        return self.remote

    def _record(self, verb, skill_id):
        self.calls.append((verb, skill_id))
        if skill_id in self.failing_ids:
            raise OpenWebUIError(400, "bad")

    def create_skill(self, form):
        self._record("create", form["id"])

    def update_skill(self, form):
        self._record("update", form["id"])

    def delete_skill(self, skill_id):
        self._record("delete", skill_id)


def _build_form_of(name):
    return {
        "id": name,
        "name": name.title(),
        "description": name.title(),
        "content": "content of " + name,
        "meta": {"tags": []},
        "is_active": True,
    }


@pytest.fixture(autouse=True)
def _fake_registry():
    registry = {
        name: _FakeExportable(canonical_name=name, display_name=name.title())
        for name in ("alpha", "beta")
    }
    forms = {
        name: _build_form_of(name) for name in registry
    }
    with patch.object(sync, "exportable_registry", registry), patch.object(
        sync, "build_skill_form", lambda exportable: forms[
            exportable.canonical_name]
    ):
        yield forms


# pytest  ######################################################################
class TestSyncSkills:

    def test_creates_absent_skills(_):
        client = _FakeClient()
        summary = sync.sync_skills(client)

        assert summary.created == ["alpha", "beta"]
        assert client.calls == [("create", "alpha"), ("create", "beta")]

    def test_updates_changed_skill(_, _fake_registry):
        stale = dict(_fake_registry["alpha"], content="old")
        client = _FakeClient(remote=[stale, _fake_registry["beta"]])
        summary = sync.sync_skills(client)

        assert summary.updated == ["alpha"]
        assert summary.skipped == ["beta"]
        assert client.calls == [("update", "alpha")]

    def test_skips_identical_skills(_, _fake_registry):
        client = _FakeClient(remote=list(_fake_registry.values()))
        summary = sync.sync_skills(client)

        assert summary.skipped == ["alpha", "beta"]
        assert client.calls == []

    def test_dry_run_reports_but_writes_nothing(_):
        client = _FakeClient(remote=[_build_form_of("gone")])
        summary = sync.sync_skills(
            client, is_dry_run=True, should_prune=True
        )

        assert summary.created == ["alpha", "beta"]
        assert summary.pruned == ["gone"]
        assert client.calls == []

    def test_dry_run_lines_carry_dry_badge(_, caplog):
        with caplog.at_level(
            logging.DEBUG, logger=sync.LOGGER_OPEN_WEBUI_NAME
        ):
            sync.sync_skills(_FakeClient(), is_dry_run=True)

        assert caplog.records
        assert all(rec.badges == ("dry",) for rec in caplog.records)

    def test_real_run_lines_carry_no_badge(_, caplog):
        with caplog.at_level(
            logging.DEBUG, logger=sync.LOGGER_OPEN_WEBUI_NAME
        ):
            sync.sync_skills(_FakeClient())

        assert caplog.records
        assert all(rec.badges == () for rec in caplog.records)

    def test_prune_off_keeps_remote_only_skill(_):
        client = _FakeClient(remote=[_build_form_of("gone")])
        summary = sync.sync_skills(client)

        assert summary.pruned == []
        assert ("delete", "gone") not in client.calls

    def test_prune_on_deletes_remote_only_skill(_):
        client = _FakeClient(remote=[_build_form_of("gone")])
        summary = sync.sync_skills(client, should_prune=True)

        assert summary.pruned == ["gone"]
        assert ("delete", "gone") in client.calls

    def test_failure_is_counted_and_does_not_abort(_):
        client = _FakeClient(failing_ids={"alpha"})
        summary = sync.sync_skills(client)

        assert [skill_id for skill_id, _ in summary.failed] == ["alpha"]
        assert summary.failed[0][1].status == 400
        assert summary.created == ["beta"]
