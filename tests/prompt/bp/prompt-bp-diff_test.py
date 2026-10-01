"""
prompt-bp-diff_test.py

Unit Tests (using pytest) for:

- diff_blueprints()
"""

from kaye_engine.prompt.blueprint.data import Blueprint
from kaye_engine.prompt.blueprint.diff import BlueprintDiff, diff_blueprints


def _bp(*labels):
    return Blueprint(nodes=frozenset((label,) for label in labels))


class TestContent:

    def test_identical_have_no_difference(_):
        out = diff_blueprints(_bp("A", "B"), _bp("A", "B"))

        assert out == BlueprintDiff(frozenset(), frozenset())

    def test_disjoint_split_by_side(_):
        out = diff_blueprints(_bp("A"), _bp("B"))

        assert out.only_left == {("A",)}
        assert out.only_right == {("B",)}

    def test_overlap_keeps_only_the_unshared(_):
        out = diff_blueprints(_bp("A", "B"), _bp("B", "C"))

        assert out.only_left == {("A",)}
        assert out.only_right == {("C",)}

    def test_empty_side(_):
        out = diff_blueprints(Blueprint(), _bp("A"))

        assert out.only_left == frozenset()
        assert out.only_right == {("A",)}

    def test_unpacks_as_a_pair(_):
        only_left, only_right = diff_blueprints(_bp("A"), _bp("B"))

        assert (only_left, only_right) == ({("A",)}, {("B",)})


class TestPurity:

    def test_inputs_are_untouched(_):
        left, right = _bp("A", "B"), _bp("B", "C")

        diff_blueprints(left, right)

        assert left == _bp("A", "B")
        assert right == _bp("B", "C")

    def test_swapping_sides_swaps_result(_):
        left, right = _bp("A", "B"), _bp("B", "C")

        forward = diff_blueprints(left, right)
        backward = diff_blueprints(right, left)

        assert forward.only_left == backward.only_right
        assert forward.only_right == backward.only_left
