"""
vs_code_settings_test.py

Unit Tests (using pytest) for:

update_settings_json
"""

import json
import os

import pytest

from kaye_engine.cli.claude.vs_code.settings import update_settings_json
from kaye_engine.cli.dry_run import disable_dry_run, enable_dry_run


# auxiliaries  #################################################################
@pytest.fixture(autouse=True)
def _reset_dry_run():
    disable_dry_run()
    yield
    disable_dry_run()


# pytest  ######################################################################
class TestUpdateSettingsJson:

    def test_missing_file_is_created_with_permissions(_, tmp_path):
        path = update_settings_json(tmp_path)

        data = json.loads(path.read_text(encoding="utf-8"))
        assert "permissions" in data

    def test_second_run_leaves_file_untouched(_, tmp_path):
        path = update_settings_json(tmp_path)
        os.utime(path, (1_000_000, 1_000_000))

        update_settings_json(tmp_path)
        assert path.stat().st_mtime == 1_000_000

    def test_stale_permissions_are_rewritten(_, tmp_path):
        path = update_settings_json(tmp_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        data["permissions"]["allow"] = []
        path.write_text(json.dumps(data), encoding="utf-8")

        update_settings_json(tmp_path)
        rewritten = json.loads(path.read_text(encoding="utf-8"))
        assert rewritten["permissions"]["allow"] != []

    def test_dry_run_leaves_stale_file_alone(_, tmp_path):
        path = update_settings_json(tmp_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        data["permissions"]["allow"] = []
        path.write_text(json.dumps(data), encoding="utf-8")
        stale = path.read_text(encoding="utf-8")

        enable_dry_run()
        update_settings_json(tmp_path)
        assert path.read_text(encoding="utf-8") == stale
