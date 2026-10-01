"""
prompt-bp-parse-text_test.py

Unit Tests (using pytest) for:

parse_blueprint_text
"""

import pytest

from kaye_engine.prompt.blueprint.data import (
    decode_blueprint,
    encode_blueprint,
)
from kaye_engine.prompt.blueprint.parser import parse_blueprint_text
from kaye_engine.prompt.prompt_corpus_loader import load_corpus_tree

_SOURCE = """# Project Title
## Description
Brief overview.
## Installation
Clone.
## License
MIT.
"""

FULL = """    ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     └── License"""

PARTIAL = """    ○
[x] └── Project Title
[x]     ├── Description
[ ]     ├── Installation
[x]     └── License"""

EMPTY = """    ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     └── License"""

TITLE = ("Project Title",)


# pytest fixtures  #############################################################
@pytest.fixture
def corpus():
    return load_corpus_tree([_SOURCE])


# pytest  ######################################################################
class TestParse:

    def test_full(_, corpus):
        bp = parse_blueprint_text(FULL)

        assert bp.nodes == {
            TITLE,
            (*TITLE, "Description"),
            (*TITLE, "Installation"),
            (*TITLE, "License"),
        }

    def test_partial_ignores_unchecked(_, corpus):
        bp = parse_blueprint_text(PARTIAL)

        assert bp.nodes == {TITLE, (*TITLE, "Description"), (*TITLE, "License")}

    def test_empty(_, corpus):
        assert parse_blueprint_text(EMPTY).nodes == frozenset()

    def test_only_nodes_are_set(_, corpus):
        bp = parse_blueprint_text(FULL)

        assert bp.subtrees == frozenset()
        assert bp.dependencies == ()

    def test_content_preview_lines_skipped(_, corpus):
        text = FULL.replace(
            "[x]     ├── Description",
            "[x]     ├── Description\n    │   Brief overview.",
        )

        assert parse_blueprint_text(text) == parse_blueprint_text(FULL)

    def test_empty_text(_, corpus):
        assert parse_blueprint_text("").nodes == frozenset()

    def test_json_round_trip(_, corpus):
        bp = parse_blueprint_text(PARTIAL)

        assert decode_blueprint(encode_blueprint(bp)) == bp


class TestNoCorpus:

    def test_parses_without_corpus(_):
        # the text alone carries the structure: no corpus is needed
        assert parse_blueprint_text(PARTIAL).nodes == {
            TITLE,
            (*TITLE, "Description"),
            (*TITLE, "License"),
        }

    def test_malformed_still_raises(_):
        with pytest.raises(ValueError, match="malformed tree format"):
            parse_blueprint_text("[x]     ├── Skipped Level")


class TestErr:

    def test_malformed_level_jump(_, corpus):
        text = """    ○
[ ] └── Project Title
[x]         ├── Too Deep"""

        with pytest.raises(ValueError) as exec_info:
            parse_blueprint_text(text)

        assert exec_info.value.args[0] == (
            "malformed tree format at line:\n[x]         ├── Too Deep"
        )

    def test_missing_node(_, corpus):
        text = """    ○
[ ] └── Project Title
[x]     ├── Description
[x]         ├── Installation
[x]     └── License"""

        with pytest.raises(ValueError) as exec_info:
            parse_blueprint_text(text)

        assert exec_info.value.args[0] == (
            "missing node heading 'Installation' in corpus that "
            "corresponds to this line:\n[x]         ├── Installation"
        )

    def test_unknown_heading(_, corpus):
        text = """    ○
[x] └── Project Title
[x]     ├── Nope"""

        with pytest.raises(ValueError, match="missing node heading 'Nope'"):
            parse_blueprint_text(text)

    def test_unchecked_unknown_heading_also_raises(_, corpus):
        text = """    ○
[ ] └── Nope"""

        with pytest.raises(ValueError, match="missing node heading 'Nope'"):
            parse_blueprint_text(text)


class TestDynamicNodes:

    def test_dynamic_heading(_, corpus):
        text = """    ○
[ ] └── Project Title
[x] └── (today)"""

        assert parse_blueprint_text(text).nodes == {("(today)",)}

    def test_several_dynamic_headings(_, corpus):
        text = """    ○
[x] ├── (today)
[x] ├── (decode-only-abbr)
[ ] └── Project Title"""

        assert parse_blueprint_text(text).nodes == {
            ("(today)",),
            ("(decode-only-abbr)",),
        }
