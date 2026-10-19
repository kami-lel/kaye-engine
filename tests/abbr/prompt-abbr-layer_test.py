"""
prompt-abbr-layer_test.py

Unit Tests (using pytest) for: layered population of ``AbbrData`` -- 2
``abbrs.json`` files, one per consumer, added into one instance
"""

import json
from unittest.mock import mock_open, patch

import pytest

from kaye_engine.abbr_collection import (
    AbbrData,
    AbbrMeaning,
    AbbrTags,
    AbbrWrap,
)
from kaye_engine.abbr_collection.abbr_data_loader import (
    populate_abbr_data_with_json_file,
)
from kaye_engine.prompt.blueprint.render.comment import (
    comment_line_registry,
    register_comment_line,
)


def _populate_layers(*layers):
    """
    populate one isolated :class:`AbbrData` with each of ``layers`` in
    turn, one :func:`populate_abbr_data_with_json_file` call per layer
    """
    data = AbbrData()
    for layer in layers:
        with (
            patch(
                "kaye_engine.abbr_collection.abbr_data_loader.get_abbr_data",
                return_value=data,
            ),
            patch("builtins.open", mock_open(read_data=json.dumps(layer))),
        ):
            populate_abbr_data_with_json_file("dummy-abbrs-path.json")
    return data


def _entry(priority=5, tags=(), wrap="word", **extra):
    return {"priority": priority, "tags": list(tags), "wrap": wrap, **extra}


def _only(data, abbr):
    found = [e for e in data.abbrs if e.abbr == abbr]
    assert len(found) == 1
    return found[0]


# pytest  ######################################################################
class TestAdditive:

    def test_disjoint_layers_add_up(_):
        data = _populate_layers(
            {"for example": {"abbrs": {"e.g.": _entry()}}},
            {"versus": {"abbrs": {"vs.": _entry()}}},
        )

        assert [e.abbr for e in data.abbrs] == ["e.g.", "vs."]
        assert [m.mean for m in data.meanings] == ["for example", "versus"]

    def test_later_layer_adds_abbr_to_known_meaning(_):
        data = _populate_layers(
            {"for example": {"remark": "r", "abbrs": {"e.g.": _entry()}}},
            {"for example": {"abbrs": {"eg": _entry()}}},
        )

        assert len(data.meanings) == 1
        assert _only(data, "eg").mean is _only(data, "e.g.").mean
        assert _only(data, "eg").mean.remark == "r"

    def test_automaton_holds_both_layers(_):
        data = _populate_layers(
            {"for example": {"abbrs": {"e.g.": _entry()}}},
            {"versus": {"abbrs": {"vs.": _entry()}}},
        )

        assert data.automaton.exists("e.g.")
        assert data.automaton.exists("vs.")


class TestTagMerge:

    def test_repeat_adds_glossary(_):
        later = _entry(tags=["other-glossary"])
        data = _populate_layers(
            {"for example": {"abbrs": {"e.g.": _entry(tags=["g"])}}},
            {"for example": {"abbrs": {"e.g.": later}}},
        )

        entry = _only(data, "e.g.")
        assert entry.glossaries == ("g", "other-glossary")
        assert len(data.abbrs) == 1

    def test_repeat_adds_flag(_):
        data = _populate_layers(
            {"for example": {"abbrs": {"e.g.": _entry(tags=["ascii_only"])}}},
            {"for example": {"abbrs": {"e.g.": _entry(tags=["common"])}}},
        )

        tags = _only(data, "e.g.").tags
        assert AbbrTags.ascii_only in tags
        assert AbbrTags.common in tags

    def test_repeated_tag_is_ignored(_):
        data = _populate_layers(
            {"for example": {"abbrs": {"e.g.": _entry(tags=["g", "common"])}}},
            {"for example": {"abbrs": {"e.g.": _entry(tags=["g", "common"])}}},
        )

        entry = _only(data, "e.g.")
        assert entry.glossaries == ("g",)
        assert entry.tags == AbbrTags.common


class TestMismatch:

    def test_priority_mismatch_raises(_):
        with pytest.raises(ValueError, match="priority"):
            _populate_layers(
                {"for example": {"abbrs": {"e.g.": _entry(priority=5)}}},
                {"for example": {"abbrs": {"e.g.": _entry(priority=6)}}},
            )

    def test_wrap_mismatch_raises(_):
        with pytest.raises(ValueError, match="wrap"):
            _populate_layers(
                {"for example": {"abbrs": {"e.g.": _entry(wrap="word")}}},
                {"for example": {"abbrs": {"e.g.": _entry(wrap="prefix")}}},
            )

    def test_duplicate_within_one_layer_raises(_):
        data = AbbrData()
        mean = AbbrMeaning("for example")

        with pytest.raises(ValueError, match="duplicate"):
            with data:
                data.add_entry(mean, "e.g.", _entry())
                data.add_entry(mean, "e.g.", _entry())


class TestRemark:

    def test_meaning_remark_filled_by_later_layer(_):
        data = _populate_layers(
            {"for example": {"abbrs": {"e.g.": _entry()}}},
            {"for example": {"remark": "late", "abbrs": {"e.g.": _entry()}}},
        )

        assert data.meanings[0].remark == "late"
        assert _only(data, "e.g.").mean.remark == "late"

    def test_meaning_remark_kept_when_omitted_later(_):
        data = _populate_layers(
            {"for example": {"remark": "early", "abbrs": {"e.g.": _entry()}}},
            {"for example": {"abbrs": {"e.g.": _entry()}}},
        )

        assert data.meanings[0].remark == "early"

    def test_meaning_remark_conflict_raises(_):
        with pytest.raises(ValueError, match="conflicting remark"):
            _populate_layers(
                {"for example": {"remark": "a", "abbrs": {"e.g.": _entry()}}},
                {"for example": {"remark": "b", "abbrs": {"e.g.": _entry()}}},
            )

    def test_entry_remark_filled_by_later_layer(_):
        data = _populate_layers(
            {"for example": {"abbrs": {"e.g.": _entry()}}},
            {"for example": {"abbrs": {"e.g.": _entry(remark="late")}}},
        )

        assert _only(data, "e.g.").remark == "late"

    def test_entry_remark_matching_is_fine(_):
        data = _populate_layers(
            {"for example": {"abbrs": {"e.g.": _entry(remark="same")}}},
            {"for example": {"abbrs": {"e.g.": _entry(remark="same")}}},
        )

        assert _only(data, "e.g.").remark == "same"

    def test_entry_remark_conflict_raises(_):
        with pytest.raises(ValueError, match="conflicting remark"):
            _populate_layers(
                {"for example": {"abbrs": {"e.g.": _entry(remark="a")}}},
                {"for example": {"abbrs": {"e.g.": _entry(remark="b")}}},
            )

    def test_wrap_value_kept(_):
        data = _populate_layers(
            {"for example": {"abbrs": {"e.g.": _entry()}}},
            {"for example": {"abbrs": {"e.g.": _entry()}}},
        )

        assert _only(data, "e.g.").wrap == AbbrWrap("word")


class TestCommentLineLayers:

    @pytest.fixture(autouse=True)
    def _restore(_):
        saved = list(comment_line_registry)
        yield
        comment_line_registry[:] = saved

    def test_two_packages_keep_first_seen_order(_):
        register_comment_line("Package A v1")
        register_comment_line("Package B v2")
        register_comment_line("Package A v1")

        tail = comment_line_registry[-2:]
        assert tail == ["Package A v1", "Package B v2"]
