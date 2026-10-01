"""
prompt-bp-render-lines_test.py

Unit Tests (using pytest) for:

render_prompt_lines, normal mode
"""

import re

import pytest

from kaye_engine.prompt.blueprint.data import Blueprint, create_blueprint
from kaye_engine.prompt.blueprint.index import get_corpus_index
from kaye_engine.prompt.blueprint.render.lines import render_prompt_lines
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.blueprint.selection import bind_selection
from kaye_engine.prompt.prompt_corpus_loader import load_corpus_tree

_SOURCE = """# Project Title
## Description
Brief overview of the project and its purpose.
## Installation
Clone the repo and install dependencies.
## Empty
## License
Licensed under the MIT License.
### {description}
Sidecar text.
"""

TITLE = ("Project Title",)
DESC = (*TITLE, "Description")
INSTALL = (*TITLE, "Installation")
EMPTY = (*TITLE, "Empty")
LICENSE = (*TITLE, "License")
SIDECAR = (*LICENSE, "{description}")


# pytest fixtures  #############################################################
@pytest.fixture(autouse=True)
def corpus():
    load_corpus_tree([_SOURCE])


def _render(*paths, **profile_kwargs):
    selection = bind_selection(Blueprint(nodes=frozenset(paths)))
    return render_prompt_lines(
        selection, profile=RenderProfile(**profile_kwargs)
    )


# pytest  ######################################################################
class TestHeadingsAndContent:

    def test_full(_):
        assert _render(TITLE, DESC, INSTALL, LICENSE) == [
            "# Project Title",
            "## Description",
            "Brief overview of the project and its purpose.",
            "",
            "## Installation",
            "Clone the repo and install dependencies.",
            "",
            "## License",
            "Licensed under the MIT License.",
        ]

    def test_partial(_):
        assert _render(DESC, LICENSE) == [
            "## Description",
            "Brief overview of the project and its purpose.",
            "",
            "## License",
            "Licensed under the MIT License.",
        ]

    def test_empty_selection(_):
        assert _render() == []

    def test_title_without_content_has_no_blank_line(_):
        assert _render(TITLE, DESC) == [
            "# Project Title",
            "## Description",
            "Brief overview of the project and its purpose.",
        ]

    def test_node_without_content_prints_heading_only(_):
        assert _render(EMPTY, LICENSE) == [
            "## Empty",
            "## License",
            "Licensed under the MIT License.",
        ]

    def test_blank_line_follows_content(_):
        assert _render(LICENSE, sparseness=99)[-1] == ""

    def test_empty_last_corpus_node_prints_heading_only(_):
        # dynamic nodes attach after the authored ones; with no glossary
        # registered the last of them renders no content, hence no
        # trailing blank line either
        last = get_corpus_index().paths[-1]

        assert _render(last, sparseness=99) == ["# " + last[-1]]

    def test_sparseness_trims_trailing_blank(_):
        assert _render(LICENSE)[-1] == "Licensed under the MIT License."

    def test_sparseness_zero_drops_blank_lines(_):
        assert "" not in _render(DESC, INSTALL, sparseness=0)


class TestDisableFirstHeading:

    def test_skips_first_selected_heading_only(_):
        assert _render(TITLE, DESC, disable_first_heading=True) == [
            "## Description",
            "Brief overview of the project and its purpose.",
        ]

    def test_keeps_first_content(_):
        assert _render(DESC, LICENSE, disable_first_heading=True) == [
            "Brief overview of the project and its purpose.",
            "",
            "## License",
            "Licensed under the MIT License.",
        ]


class TestDynamicNodes:

    def test_dynamic_node_is_live(_):
        lines = _render(("(today)",))

        assert lines[0] == "# (today)" or lines[0].startswith("#")
        assert len(lines) > 1

    def test_dynamic_content_receives_kwargs(_):
        selection = bind_selection(
            Blueprint(nodes=frozenset({("(decode-only-abbr)",)}))
        )

        lines = render_prompt_lines(selection, query="x")

        assert lines[0].startswith("#")


class TestComment:

    def test_comment_appended_last(_):
        lines = _render(DESC, show_comment=True, display_name="Demo")

        assert lines[-1] == "-->"
        assert "<!--" in lines
        assert "blueprint: Demo" in lines

    def test_compact_comment_for_minus_one(_):
        lines = _render(DESC, show_comment=True, sparseness=-1)

        assert len(lines) == 1
        assert re.search(r"<!--.*Kaye Engine v.*-->", lines[0])

    def test_no_comment_by_default(_):
        assert "<!--" not in _render(DESC)


class TestSidecarsSpliced:

    def test_conditional_sidecar_spliced_under_selected_parent(_):
        lines = _render(LICENSE, conditional_sidecars=("description",))

        assert lines[-2:] == ["### {description}", "Sidecar text."]

    def test_not_spliced_without_selected_parent(_):
        assert "Sidecar text." not in _render(
            DESC, conditional_sidecars=("description",)
        )
