"""
test for ``load_embedded_prompt_corpus``
"""

from os.path import dirname, abspath, join, normpath

from kaye.gen_prompt import (
    load_embedded_prompt_corpus,
    get_embedded_prompt_corpus_file_path,
    PromptCorpusNode,
)


class TestGet:  # test function get_embedded_prompt_corpus_file_path

    def test1(_):
        submission = get_embedded_prompt_corpus_file_path()
        solution = normpath(
            join(
                dirname(abspath(__file__)),
                "../../../kaye/kaye/prompt_corpus.md",
            )
        )
        print("submission:\t{}\nsolution:\t{}".format(submission, solution))
        assert str(submission) == solution


class TestLoad:  # test function load_embedded_prompt_corpus
    def test_type(_):
        opt = load_embedded_prompt_corpus()
        assert isinstance(opt, PromptCorpusNode)
