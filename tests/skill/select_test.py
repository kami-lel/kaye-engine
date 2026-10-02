"""
select_test.py

Unit Tests (using pytest) for:

select_exportables() name resolution
"""

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from kaye_engine.skill import select
from kaye_engine.skill.select import select_exportables


# auxiliaries  #################################################################
@pytest.fixture(name="_registry")
def _registry_fixture():
    registry = {
        name: SimpleNamespace(canonical_name=name)
        for name in ("alpha", "beta", "gamma")
    }
    with patch.object(select, "exportable_registry", registry):
        yield registry


# pytest  ######################################################################
class TestSelectExportables:

    def test_none_selects_all_in_registry_order(_, _registry):
        assert select_exportables() == list(_registry.values())

    def test_names_select_in_order_named(_, _registry):
        picked = select_exportables(["gamma", "alpha"])

        assert [e.canonical_name for e in picked] == ["gamma", "alpha"]

    def test_repeated_name_selected_once(_, _registry):
        picked = select_exportables(["beta", "beta"])

        assert [e.canonical_name for e in picked] == ["beta"]

    def test_unknown_names_all_listed(_, _registry):
        with pytest.raises(ValueError, match="nope, zilch") as info:
            select_exportables(["alpha", "nope", "zilch"])

        assert "alpha" not in str(info.value)
