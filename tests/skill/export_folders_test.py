"""
export_folders_test.py

Unit Tests (using pytest) for:

export_skills_as_folders() name selection
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from kaye_engine.skill import export_folders, select
from kaye_engine.skill.export_folders import export_skills_as_folders


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
