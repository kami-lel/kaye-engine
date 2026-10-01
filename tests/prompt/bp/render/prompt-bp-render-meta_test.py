"""
prompt-bp-render-meta_test.py

Unit Tests (using pytest) for:

show_description, show_when_to_use,
show_description_and_when_to_use, show_globs
"""

import pytest

from kaye_engine.prompt.blueprint.data import Blueprint, BlueprintMeta
from kaye_engine.prompt.blueprint.render.meta import (
    show_dependencies,
    show_globs,
    show_description,
    show_description_and_when_to_use,
    show_when_to_use,
)
from kaye_engine.prompt.blueprint.render.util import (
    REPLACEMENT_NEWLINE_SYMBOL,
)
from kaye_engine.prompt.prompt_corpus_loader import load_corpus_tree

_SOURCE = """# Personality
## Ria
### {description}
Ria is a persona.
### {when_to_use}
Use when summoning Ria.

Second paragraph.
### {globs}
```glob
**/*.py
*.md
```
trailing text
## Bare
"""

DESC = ("Personality", "Ria", "{description}")
WHEN = ("Personality", "Ria", "{when_to_use}")
GLOBS = ("Personality", "Ria", "{globs}")
BARE = ("Personality", "Bare")


# pytest fixtures  #############################################################
@pytest.fixture(autouse=True)
def corpus():
    load_corpus_tree([_SOURCE])


def _bp(**meta):
    return Blueprint(meta=BlueprintMeta(**meta))


# pytest  ######################################################################
class TestDescription:

    def test_from_node(_):
        assert show_description(_bp(description_node=DESC)) == (
            "Ria is a persona."
        )

    def test_literal_has_priority(_):
        bp = _bp(description="Literal", description_node=DESC)

        assert show_description(bp) == "Literal"

    def test_none_set(_):
        assert show_description(_bp()) == ""

    def test_empty_node(_):
        assert show_description(_bp(description_node=BARE)) == ""

    def test_unknown_node_raises(_):
        with pytest.raises(ValueError, match="Nope"):
            show_description(_bp(description_node=("Nope",)))


class TestWhenToUse:

    def test_multi_paragraph_joined_on_one_line(_):
        out = show_when_to_use(_bp(when_to_use_node=WHEN))

        assert out == (
            "Use when summoning Ria."
            + REPLACEMENT_NEWLINE_SYMBOL * 2
            + "Second paragraph."
        )

    def test_none_set(_):
        assert show_when_to_use(_bp()) == ""


class TestDescriptionAndWhenToUse:

    def test_joined(_):
        out = show_description_and_when_to_use(
            _bp(description_node=DESC, when_to_use_node=WHEN)
        )

        assert out.startswith(
            "Ria is a persona." + REPLACEMENT_NEWLINE_SYMBOL
            + "Use when summoning Ria."
        )

    def test_literal_has_priority(_):
        out = show_description_and_when_to_use(
            _bp(description="Literal", when_to_use_node=WHEN)
        )

        assert out == "Literal"

    def test_only_when_to_use(_):
        out = show_description_and_when_to_use(_bp(when_to_use_node=WHEN))

        assert out.startswith("Use when summoning Ria.")

    def test_none_set(_):
        assert show_description_and_when_to_use(_bp()) == ""


class TestGlobs:

    def test_extracts_fenced_glob_block(_):
        assert show_globs(_bp(globs_node=GLOBS)) == ["**/*.py", "*.md"]

    def test_none_set(_):
        assert show_globs(_bp()) == []

    def test_node_without_block(_):
        assert show_globs(_bp(globs_node=DESC)) == []


class TestDependencies:

    def test_none(_):
        assert show_dependencies(Blueprint()) == ()

    def test_names_keep_order(_):
        bp = Blueprint(dependencies=("b", "a"))

        assert show_dependencies(bp) == ("b", "a")

    def test_value_dependency_shows_as_label(_):
        bp = Blueprint(dependencies=("a", Blueprint()))

        assert show_dependencies(bp) == ("a", "<blueprint value>")
