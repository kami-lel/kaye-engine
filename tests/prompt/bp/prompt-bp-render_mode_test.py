"""
prompt-bp-render_mode_test.py

Unit Tests (using pytest) for:

- RenderMode.IMAGE (heading flatten, forced sparseness)
- RenderMode.NEGATIVE via the unified entry point
- RenderMode.NEGATIVE | RenderMode.IMAGE combined
"""

from kaye_engine.prompt import PromptBlueprint
from kaye_engine.prompt.blueprint import render
from kaye_engine.prompt.blueprint.render_mode import RenderMode
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode


# auxiliaries  ##################################################################
def _build_corpus(text):
    lines = text.strip("\n").splitlines()
    return PromptCorpusNode.parse("○", None, lines)


# fixtures  ######################################################################
def _nested_heading_corpus():
    return _build_corpus(
        """
# Some
Content of Some.
## Prompt
Content of Prompt.
### Content
Content of Content.
"""
    )


def _nested_avoid_corpus():
    return _build_corpus(
        """
# Some
Content of Some.
## Prompt
Content of Prompt.
### {avoid}
AAAA
### Content
Content of Content.
#### {avoid}
BBBB
## Other
Content with no avoid anywhere below it.
"""
    )


# pytest  ########################################################################
class TestImageModeFlattensHeadings:  ############################################

    def test_flattens_headings_at_every_depth(_):
        bp = PromptBlueprint.create_full_blueprint(
            corpus_tree=_nested_heading_corpus()
        )

        opt = render.render_prompt_lines(
            bp, profile=RenderProfile(mode=RenderMode.IMAGE)
        )

        assert "# Some" not in opt
        assert "Some:" in opt
        assert "Prompt:" in opt
        assert "Content:" in opt

    def test_forces_sparseness_1_over_explicit_sparseness(_):
        bp = PromptBlueprint.create_full_blueprint(
            corpus_tree=_nested_heading_corpus()
        )

        opt = bp.generate_prompt_without_dependencies(
            profile=RenderProfile(mode=RenderMode.IMAGE, sparseness=99)
        )

        assert "\n\n\n" not in opt


class TestNegativeModeViaUnifiedEntryPoint:  ######################################

    def test_matches_dedicated_negative_lines_function(_):
        bp = PromptBlueprint.create_full_blueprint(
            corpus_tree=_nested_avoid_corpus()
        )

        via_mode = bp.generate_prompt_without_dependencies(
            profile=RenderProfile(mode=RenderMode.NEGATIVE)
        ).split("\n")
        dedicated = render.render_negative_prompt_lines(bp)

        assert via_mode == dedicated
        assert via_mode == [
            "# Some",
            "## Prompt",
            "AAAA",
            "",
            "### Content",
            "BBBB",
        ]


class TestNegativeAndImageModeCombined:  ##########################################

    def test_negative_content_with_flattened_headings(_):
        bp = PromptBlueprint.create_full_blueprint(
            corpus_tree=_nested_avoid_corpus()
        )

        opt = bp.generate_prompt_without_dependencies(
            profile=RenderProfile(mode=RenderMode.NEGATIVE | RenderMode.IMAGE)
        ).split("\n")

        assert "AAAA" in opt
        assert "BBBB" in opt
        assert not any(line.startswith("#") for line in opt)
        assert "Some:" in opt
        assert "Content:" in opt
