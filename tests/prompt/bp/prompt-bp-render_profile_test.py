"""
prompt-bp-render_profile_test.py

Unit Tests (using pytest) for:

- RenderProfile
"""

from kaye_engine.prompt.blueprint.render_profile import RenderProfile


class TestMergeConditionalSidecars:  ############################################

    def test_dedup_and_order(_):
        merged = RenderProfile(conditional_sidecars=("a", "b")).merge(
            RenderProfile(conditional_sidecars=("b", "c"))
        )
        assert merged.conditional_sidecars == ("a", "b", "c")

    def test_empty(_):
        merged = RenderProfile().merge(RenderProfile())
        assert merged.conditional_sidecars == ()


class TestMergeVariants:  #######################################################

    def test_all_none_returns_none(_):
        merged = RenderProfile(variants=None).merge(
            RenderProfile(variants=None)
        )
        assert merged.variants is None

    def test_one_none_one_tuple(_):
        merged = RenderProfile(variants=None).merge(
            RenderProfile(variants=("a", "b"))
        )
        assert merged.variants == ("a", "b")

    def test_dedup_across_groups(_):
        merged = RenderProfile(variants=("a", "b")).merge(
            RenderProfile(variants=("b", "c"))
        )
        assert merged.variants == ("a", "b", "c")


class TestMergeScalarOverride:  #################################################

    def test_other_wins(_):
        merged = RenderProfile(show_comment=False, sparseness=1).merge(
            RenderProfile(show_comment=True, sparseness=0)
        )
        assert merged.show_comment is True
        assert merged.sparseness == 0

    def test_other_default_still_wins(_):
        merged = RenderProfile(display_name="Chat").merge(RenderProfile())
        assert merged.display_name == ""


class TestAsKwargs:  ############################################################

    def test_splattable_dict(_):
        profile = RenderProfile(
            show_comment=True,
            disable_first_heading=True,
            conditional_sidecars=("a",),
            variants=("b",),
            display_name="Chat",
            sparseness=0,
            glossary_priority_threshold=2,
            is_sorted=True,
            uses_numbered_list=False,
        )
        assert profile.as_kwargs() == {
            "show_comment": True,
            "disable_first_heading": True,
            "conditional_sidecars": ("a",),
            "variants": ("b",),
            "display_name": "Chat",
            "sparseness": 0,
            "glossary_priority_threshold": 2,
            "is_sorted": True,
            "uses_numbered_list": False,
        }
