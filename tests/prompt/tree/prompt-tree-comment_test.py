"""
prompt-tree-comment_test.py

Unit Tests (using pytest) for:

load_corpus_tree, markdown comment stripping
"""

import pytest

from kaye_engine.prompt.blueprint.data import Blueprint
from kaye_engine.prompt.blueprint.render.lines import render_prompt_lines
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.blueprint.selection import bind_selection
from kaye_engine.prompt.prompt_corpus_loader import load_corpus_tree

from tests.corpus_helper import load_corpus_from_sources

_SOURCE = """# Title

<!--
TODO note a
TODO note b
-->


Body text with `<!-- Endnotes -->` mention.
<!-- single note -->

```md
<!-- fenced stays -->
```

<example>
<!-- tagged stays -->
</example>
"""

TITLE = ("Title",)


def _body():
    tree = load_corpus_from_sources([_SOURCE])
    return list(tree.children[0].content_lines())


# pytest  ######################################################################
class TestCommentStripping:

    def test_comment_lines_absent_from_content(_):
        body = _body()
        assert "TODO note a" not in "\n".join(body)
        assert "<!-- single note -->" not in body

    def test_blank_run_after_removed_comment_collapses(_):
        body = _body()
        assert body[0] == ""
        assert body[1] == "Body text with `<!-- Endnotes -->` mention."

    def test_inline_code_fenced_and_tagged_comments_kept(_):
        body = _body()
        assert "Body text with `<!-- Endnotes -->` mention." in body
        assert "<!-- fenced stays -->" in body
        assert "<!-- tagged stays -->" in body


class TestRenderedComment:

    @pytest.mark.parametrize("show_comment", [True, False])
    def test_only_generated_comment_renders(_, show_comment):
        load_corpus_from_sources([_SOURCE.split("```md")[0]])
        selection = bind_selection(Blueprint(nodes=frozenset({TITLE})))
        lines = render_prompt_lines(
            selection,
            profile=RenderProfile(show_comment=show_comment, sparseness=1),
        )
        text = "\n".join(lines)

        assert "TODO note" not in text
        assert "single note" not in text
        openers = [line for line in lines if line.startswith("<!--")]
        assert len(openers) == int(show_comment)
