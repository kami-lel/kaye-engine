"""
prompt-bp-negative_prompt_test.py

Unit Tests (using pytest) for:

- render.render_negative_prompt_lines()
- PromptBlueprint.generate_negative_prompt_without_dependencies()
"""

import re

from kaye_engine.prompt import PromptBlueprint
from kaye_engine.prompt.blueprint import render
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode


# auxiliaries  ##################################################################
def _build_corpus(text):
    lines = text.strip("\n").splitlines()
    return PromptCorpusNode.parse("○", None, lines)


# fixtures  ######################################################################
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
class TestNestedAvoidStructure:  ################################################

    def test_shows_surrounding_headings_never_the_avoid_heading(_):
        bp = PromptBlueprint.create_full_blueprint(
            corpus_tree=_nested_avoid_corpus()
        )

        opt = render.render_negative_prompt_lines(bp)

        print(opt)
        assert opt == [
            "# Some",
            "## Prompt",
            "AAAA",
            "",
            "### Content",
            "BBBB",
        ]

    def test_branch_without_avoid_content_is_fully_omitted(_):
        bp = PromptBlueprint.create_full_blueprint(
            corpus_tree=_nested_avoid_corpus()
        )

        opt = render.render_negative_prompt_lines(bp)

        assert not any("Other" in line for line in opt)


class TestUncheckmarkedNodeOmitted:  #############################################

    def test_avoid_under_uncheckmarked_node_is_dropped(_):
        bp = PromptBlueprint.create_full_blueprint(
            corpus_tree=_nested_avoid_corpus()
        )
        bp.uncheckmark(bp.corpus["Some"]["Prompt"]["Content"])

        opt = render.render_negative_prompt_lines(bp)

        print(opt)
        assert opt == ["# Some", "## Prompt", "AAAA"]

    def test_ancestor_still_checkmarked_keeps_its_own_avoid(_):
        bp = PromptBlueprint.create_full_blueprint(
            corpus_tree=_nested_avoid_corpus()
        )
        bp.uncheckmark(bp.corpus["Some"]["Prompt"]["Content"])

        opt = render.render_negative_prompt_lines(bp)

        assert "AAAA" in opt
        assert "BBBB" not in opt


class TestMultipleSiblingsContribute:  ###########################################

    def _corpus(_):
        return _build_corpus(
            """
# Some
## Prompt
### {avoid}
AAAA
## Other
### {avoid}
CCCC
"""
        )

    def test_sibling_blocks_are_blank_line_separated(_):
        bp = PromptBlueprint.create_full_blueprint(corpus_tree=_._corpus())

        opt = render.render_negative_prompt_lines(bp)

        print(opt)
        assert opt == [
            "# Some",
            "## Prompt",
            "AAAA",
            "",
            "## Other",
            "CCCC",
        ]


class TestShowCommentAndSparseness:  #############################################

    def test_show_comment_appends_comment_line(_):
        bp = PromptBlueprint.create_full_blueprint(
            corpus_tree=_nested_avoid_corpus()
        )

        opt = render.render_negative_prompt_lines(
            bp, profile=RenderProfile(show_comment=True)
        )

        print(opt)
        assert re.fullmatch("<!-- Kaye Engine v.+ -->", opt[-1])

    def test_sparseness_minus_one_collapses_to_one_line(_):
        bp = PromptBlueprint.create_full_blueprint(
            corpus_tree=_nested_avoid_corpus()
        )

        opt = render.render_negative_prompt_lines(
            bp, profile=RenderProfile(sparseness=-1)
        )

        assert len(opt) == 1


class TestGenerateNegativePromptWithoutDependencies:  ############################

    def test_returns_joined_string(_):
        bp = PromptBlueprint.create_full_blueprint(
            corpus_tree=_nested_avoid_corpus()
        )

        opt = bp.generate_negative_prompt_without_dependencies()

        print(opt)
        assert opt == "# Some\n## Prompt\nAAAA\n\n### Content\nBBBB"

    def test_no_avoid_anywhere_renders_empty(_):
        bp = PromptBlueprint.create_full_blueprint(
            corpus_tree=_build_corpus(
                """
# Some
Nothing to avoid here.
"""
            )
        )

        opt = bp.generate_negative_prompt_without_dependencies()

        assert opt == ""
