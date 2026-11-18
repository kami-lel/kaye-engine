"""
vs_code_export_test.py

Unit Tests (using pytest) for:

export_vs_code_extension() build-in-tmp and publish log phases
"""

import logging
from pathlib import Path
from unittest.mock import patch

import kamilog

from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.vs_code import export as export_module
from kaye_engine.cli.claude.vs_code.export import export_vs_code_extension
from kaye_engine.deed import track


def _fake_generate(payload, render_profile=None):
    # one scratch deed and one real file, as the payload build would log
    with track(kamilog.getLogger(LOGGER_CLAUDE_NAME)).create_file(
        Path(payload) / "CLAUDE.md"
    ):
        (Path(payload) / "CLAUDE.md").write_text("x", encoding="utf-8")


def _run(tmp_path, caplog, level):
    caplog.set_level(level, logger=LOGGER_CLAUDE_NAME)
    with patch.object(
        export_module, "generate_vs_code_payload", _fake_generate
    ), patch.object(
        export_module, "place_vs_code_payload", lambda *_: tmp_path / "m.json"
    ):
        return export_vs_code_extension(tmp_path / "claude")


class TestExportPhases:

    def test_build_and_publish_phases_are_entered(_, tmp_path, caplog):
        _run(tmp_path, caplog, kamilog.ENTER)

        entered = [
            r.message for r in caplog.records if r.levelno == kamilog.ENTER
        ]
        assert entered[0].startswith("build payload in tmp")
        assert entered[1].startswith("publish payload into")

    def test_scratch_deed_wears_tmp_badge_with_masked_root(
        _, tmp_path, caplog
    ):
        _run(tmp_path, caplog, logging.DEBUG)

        scratch = [r for r in caplog.records if r.message.startswith("create")]
        assert [r.message for r in scratch] == ["create <tmp>/CLAUDE.md"]
        assert scratch[0].badges == ("tmp",)
        assert scratch[0].levelno == logging.DEBUG

    def test_one_tmp_summary_at_info(_, tmp_path, caplog):
        _run(tmp_path, caplog, logging.INFO)

        summaries = [
            r for r in caplog.records if r.message.startswith("build payload")
        ]
        assert [r.message for r in summaries] == ["build payload (1 files)"]
        assert summaries[0].badges == ("tmp",)
