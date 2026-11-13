"""
export_folders_test.py

Unit Tests (using pytest) for:

export_skills_as_folders() name selection
"""

import logging
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
import yaml

from kaye_engine.consumer import register_consumer
from kaye_engine.prompt.blueprint import BlueprintRegistry
from kaye_engine.prompt.blueprint.data import Blueprint, BlueprintMeta
from kaye_engine.skill import LOGGER_SKILL_NAME, export_folders, select
from kaye_engine.skill.export_folders import export_skills_as_folders

from tests.consumer_helper import isolated_consumers


# auxiliaries  #################################################################
@pytest.fixture(name="_written")
def _written_fixture(tmp_path):
    """names of the skills written, with a two-entry registry patched in"""
    registry = {
        name: SimpleNamespace(canonical_name=name, display_name=name)
        for name in ("alpha", "beta")
    }
    written = []

    def _from_exportable(exportable, **_kwargs):
        skill = MagicMock()
        skill.write.side_effect = lambda _: written.append(
            exportable.canonical_name
        )
        return skill

    with (
        patch.object(select, "exportable_registry", registry),
        patch.object(
            export_folders.Skill,
            "from_exportable",
            side_effect=_from_exportable,
        ),
    ):
        yield written


# pytest  ######################################################################
class TestExportSkillsAsFolders:

    def test_default_exports_every_entry(_, _written, tmp_path):
        export_skills_as_folders(tmp_path, version="1")

        assert _written == ["alpha", "beta"]

    def test_names_export_only_those(_, _written, tmp_path):
        export_skills_as_folders(tmp_path, version="1", names=["beta"])

        assert _written == ["beta"]

    def test_unknown_name_writes_nothing(_, _written, tmp_path):
        with pytest.raises(ValueError, match="nope"):
            export_skills_as_folders(
                tmp_path, version="1", names=["alpha", "nope"]
            )

        assert not _written


class TestOwnerVersion:
    """each skill carries the version of the consumer owning its entry"""

    def test_each_skill_takes_its_owners_version(_, tmp_path):
        with isolated_consumers():
            register_consumer("Alpha", "alpha-pkg", "1.0.0")
            register_consumer("Beta", "beta-pkg", "2.5.0")
            _._export_and_check(tmp_path)

    @staticmethod
    def _export_and_check(tmp_path):
        registry = {
            name: BlueprintRegistry(
                canonical_name=name,
                display_name=name,
                blueprint=Blueprint(meta=BlueprintMeta(description="d")),
                consumer=owner,
            )
            for name, owner in (("one", "alpha-pkg"), ("two", "beta-pkg"))
        }
        with (
            patch.object(select, "exportable_registry", registry),
            patch.object(BlueprintRegistry, "content", return_value="body"),
        ):
            export_skills_as_folders(tmp_path)

        versions = {
            name: yaml.safe_load(
                (tmp_path / name / "SKILL.md").read_text().split("---")[1]
            )["metadata"]["version"]
            for name in registry
        }
        assert versions == {"one": "1.0.0", "two": "2.5.0"}


class TestEnterLine:

    @staticmethod
    def _enter_messages(caplog, **kwargs):
        registry = {
            "alpha": SimpleNamespace(
                canonical_name="alpha", display_name="alpha", consumer="proj-a"
            )
        }
        with (
            patch.object(select, "exportable_registry", registry),
            patch.object(export_folders.Skill, "from_exportable"),
            caplog.at_level(logging.DEBUG, logger=LOGGER_SKILL_NAME),
        ):
            export_skills_as_folders(".", version="1", **kwargs)
        return [rec.message for rec in caplog.records]

    def test_names_the_consumer_when_given(_, caplog):
        messages = TestEnterLine._enter_messages(caplog, consumer="proj-a")

        assert messages == ["exporting exportables as skills:\tproj-a"]

    def test_plain_line_without_a_consumer(_, caplog):
        messages = TestEnterLine._enter_messages(caplog)

        assert messages == ["exporting exportables as skills"]


class TestMultipleDestinations:

    def test_single_render_writes_every_destination(_, tmp_path):
        skill = export_folders.Skill(name="alpha", body="b", version="1")
        dests = [tmp_path / "a", tmp_path / "b"]
        with patch.object(
            export_folders.Skill, "render", wraps=skill.render
        ) as render:
            folders = skill.write(dests)

        assert render.call_count == 1
        assert folders == [d / "alpha" for d in dests]
        texts = {(f / "SKILL.md").read_text(encoding="utf-8") for f in folders}
        assert len(texts) == 1

    def test_path_still_accepted(_, tmp_path):
        skill = export_folders.Skill(name="alpha", body="b", version="1")

        assert skill.write(tmp_path) == [tmp_path / "alpha"]
