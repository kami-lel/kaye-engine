"""
parser_test.py

Unit Tests (using pytest) for:

the ``skill`` subcommand: argument shapes, name resolution, export dispatch
"""

from argparse import ArgumentParser
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from kaye_engine.cli.skill import parser as skill_cli
from kaye_engine.skill import select


# auxiliaries  #################################################################
def _parse_and_run(argv):
    parser = ArgumentParser()
    skill_cli.register_skill_parser(parser.add_subparsers())
    args = parser.parse_args(["skill", *argv])
    args.func(args)


@pytest.fixture(name="_calls")
def _calls_fixture():
    registry = {
        name: SimpleNamespace(canonical_name=name)
        for name in ("alpha", "beta")
    }
    with (
        patch.object(select, "exportable_registry", registry),
        patch.object(skill_cli, "check_corpus_setup_for_cli"),
        patch.object(
            skill_cli, "get_consumer_version", return_value="1"
        ),
        patch.object(skill_cli, "export_skills_as_folders") as folders,
        patch.object(skill_cli, "export_skills_as_zips") as zips,
    ):
        yield SimpleNamespace(folders=folders, zips=zips)


# pytest  ######################################################################
class TestSkillParser:

    def test_names_then_folder(_, _calls, tmp_path):
        _parse_and_run(["alpha", "beta", str(tmp_path)])

        kwargs = _calls.folders.call_args.kwargs
        assert _calls.folders.call_args.args == (tmp_path,)
        assert kwargs["names"] == ["alpha", "beta"]
        assert not _calls.zips.called

    def test_all_exports_everything(_, _calls, tmp_path):
        _parse_and_run(["--all", str(tmp_path)])

        assert _calls.folders.call_args.kwargs["names"] is None

    def test_short_all_flag(_, _calls, tmp_path):
        _parse_and_run(["-a", str(tmp_path)])

        assert _calls.folders.call_args.kwargs["names"] is None

    def test_zip_routes_to_zip_export(_, _calls, tmp_path):
        _parse_and_run(["-z", "alpha", str(tmp_path)])

        assert _calls.zips.call_args.kwargs["names"] == ["alpha"]
        assert not _calls.folders.called

    def test_missing_folder_is_a_usage_error(_, _calls):
        with pytest.raises(SystemExit) as info:
            _parse_and_run([])

        assert info.value.code == 2

    def test_names_without_all_need_a_name(_, _calls, tmp_path):
        with pytest.raises(SystemExit) as info:
            _parse_and_run([str(tmp_path)])

        assert info.value.code == 2
        assert not _calls.folders.called

    def test_all_with_names_is_a_usage_error(_, _calls, tmp_path):
        with pytest.raises(SystemExit) as info:
            _parse_and_run(["--all", "alpha", str(tmp_path)])

        assert info.value.code == 2
        assert not _calls.folders.called

    def test_unknown_name_exits_1_writing_nothing(_, _calls, tmp_path):
        with pytest.raises(SystemExit) as info:
            _parse_and_run(["alpha", "nope", str(tmp_path)])

        assert info.value.code == 1
        assert not _calls.folders.called
