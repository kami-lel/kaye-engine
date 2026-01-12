"""
prompt_blueprint_init_test.py

Unit Tests (using pytest) for: PromptBlueprint.__init__()
"""

from kaye.gen_prompt import PromptBlueprint, load_embedded_prompt_corpus


def test_dft():
    corpus = load_embedded_prompt_corpus()

    empty_bp = PromptBlueprint(corpus)

    print(empty_bp)

    assert isinstance(empty_bp, dict)
    assert len(empty_bp) == 0
    assert empty_bp.corpus is corpus
    assert isinstance(empty_bp.display_name, str)
    assert empty_bp.display_name == ""


def test_name():
    corpus = load_embedded_prompt_corpus()
    name = "My Blueprint"

    empty_bp = PromptBlueprint(corpus, display_name=name)

    print(empty_bp)

    assert isinstance(empty_bp, dict)
    assert len(empty_bp) == 0
    assert empty_bp.corpus is corpus
    assert isinstance(empty_bp.display_name, str)
    assert empty_bp.display_name == name
