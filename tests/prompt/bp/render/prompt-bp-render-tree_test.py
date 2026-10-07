"""
prompt-bp-render-tree_test.py

Unit Tests (using pytest) for:

preview_selection
"""

import re

import pytest

from kaye_engine.prompt.blueprint.data import Blueprint
from kaye_engine.prompt.blueprint.parser import parse_blueprint_tree
from kaye_engine.prompt.blueprint.render.tree import preview_selection
from kaye_engine.prompt.blueprint.selection import bind_selection
from kaye_engine.prompt.prompt_corpus_loader import load_corpus_tree

_SOURCE = """# Project Title
## Description
Brief overview of the project and its purpose.
## Installation
Clone the repo and install dependencies.
## License
Licensed under the MIT License.
"""

TITLE = ("Project Title",)
DESC = (*TITLE, "Description")
INSTALL = (*TITLE, "Installation")
LICENSE = (*TITLE, "License")


# pytest fixtures  #############################################################
@pytest.fixture(autouse=True)
def corpus():
    load_corpus_tree([_SOURCE])


def _select(*paths):
    return bind_selection(Blueprint(nodes=frozenset(paths)))


# pytest  ######################################################################
class TestPrunedTree:

    def test_selected_nodes_and_ancestors(_):
        out = preview_selection(
            _select(DESC, LICENSE), content_preview_lines=0
        )

        assert out == """    ○
[ ] └── Project Title
[x]     ├── Description
[x]     └── License"""

    def test_ancestor_shown_unchecked(_):
        out = preview_selection(
            _select(INSTALL), content_preview_lines=0
        )

        assert "[ ] └── Project Title" in out
        assert "[x]     └── Installation" in out

    def test_full_selection(_):
        out = preview_selection(
            _select(TITLE, DESC, INSTALL, LICENSE), content_preview_lines=0
        )

        assert out == """    ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     └── License"""

    def test_empty_selection_is_only_root(_):
        assert preview_selection(_select()) == "    ○"

    def test_connectors_for_middle_and_last_child(_):
        out = preview_selection(
            _select(DESC, INSTALL), content_preview_lines=0
        )

        assert "├── Description" in out
        assert "└── Installation" in out


class TestFullTree:

    def test_unselected_nodes_shown(_):
        out = preview_selection(
            _select(DESC), show_full_tree=True, content_preview_lines=0
        )

        assert re.search(r"^\[x\] .*├── Description$", out, re.M)
        assert re.search(r"^\[ \] .*├── Installation$", out, re.M)
        assert re.search(r"^\[ \] .*└── License$", out, re.M)


class TestContentPreview:

    def test_preview_lines(_):
        out = preview_selection(_select(DESC, LICENSE))

        assert """[x]     ├── Description
        │   Brief overview of the project and its purpose.
[x]     └── License
            Licensed under the MIT License.""" in out

    def test_preview_width_cut(_):
        out = preview_selection(
            _select(DESC), content_preview_width=20
        )

        assert "Brief ov" in out
        assert "Brief overview" not in out

    def test_preview_line_limit(_):
        out = preview_selection(_select(DESC), content_preview_lines=1)

        assert out.count("Brief overview") == 1


class TestComment:

    def test_comment_appended(_):
        out = preview_selection(
            _select(DESC), show_comment=True, display_name="Demo"
        )

        assert re.search(r"<!--\nblueprint: Demo\nKaye Engine v.+\n-->$", out)

    def test_no_comment_by_default(_):
        assert "<!--" not in preview_selection(_select(DESC))


class TestRoundTrip:

    @pytest.mark.parametrize(
        "paths",
        [(), (DESC,), (TITLE, INSTALL), (DESC, INSTALL, LICENSE)],
    )
    def test_tree_parses_back_to_equal_blueprint(_, paths):
        blueprint = Blueprint(nodes=frozenset(paths))

        text = preview_selection(
            bind_selection(blueprint), content_preview_lines=0
        )

        assert parse_blueprint_tree(text) == blueprint

    def test_full_tree_with_previews_parses_back(_):
        blueprint = Blueprint(nodes=frozenset({DESC, LICENSE}))

        text = preview_selection(
            bind_selection(blueprint), show_full_tree=True
        )

        assert parse_blueprint_tree(text) == blueprint

    def test_dynamic_nodes_round_trip(_):
        blueprint = Blueprint(nodes=frozenset({("(today)",), DESC}))

        text = preview_selection(
            bind_selection(blueprint), content_preview_lines=0
        )

        assert parse_blueprint_tree(text) == blueprint
