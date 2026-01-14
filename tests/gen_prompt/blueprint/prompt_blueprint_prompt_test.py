"""
prompt_blueprint_prompt_test.py

Unit Tests (using pytest) for: PromptBlueprint.generate_prompt()
"""

import re


from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode

from tests.gen_prompt import PROMPT1, PROMPT2, PROMPT3
from tests.gen_prompt.blueprint import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_FULL_PREVIEW,
    BLUEPRINT_1_EMPTY,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_1_PREVIEW,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_1_PARTIAL_2_PREVIEW,
    BLUEPRINT_1_PARTIAL_2_PRUNED,
    BLUEPRINT_2_FULL,
    BLUEPRINT_2_PREVIEW,
    BLUEPRINT_2_PARTIAL_1,
    BLUEPRINT_2_PARTIAL_1_PREVIEW,
    BLUEPRINT_2_PARTIAL_1_PRUNED,
    BLUEPRINT_2_EMPTY,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_FULL_PREVIEW,
    BLUEPRINT_3_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_1_PREVIEW,
    BLUEPRINT_3_PARTIAL_1_PRUNED,
    BLUEPRINT_3_PARTIAL_2,
    BLUEPRINT_3_PARTIAL_2_PREVIEW,
    BLUEPRINT_3_PARTIAL_2_PRUNED,
    BLUEPRINT_3_EMPTY,
    _split_content_and_comment,
)


class Test1:  # with PROMPT1  ##################################################

    corpus = PromptCorpusNode.parse(PROMPT1)

    def test_full(self):
        bp_text = BLUEPRINT_1_FULL
        bp = PromptBlueprint.parse(self.corpus, bp_text)

        opt = bp.generate_prompt(hide_comment=False)

        print(opt)
        content, comment = _split_content_and_comment(opt)
        assert content == """# Project Title

## Description
Brief overview of the project and its purpose.

## Installation
Clone the repo and install dependencies.

## License
Licensed under the MIT License."""

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment)

    # TODO

    def test_part1(_):

        bp_text = BLUEPRINT_1_PARTIAL_1

    def test_part2(_):
        bp_text = BLUEPRINT_1_PARTIAL_2

    def test_empty(_):
        bp_text = BLUEPRINT_1_EMPTY


class Test2:  # with PROMPT2  ##################################################

    corpus = PromptCorpusNode.parse(PROMPT2)

    def test_full(self):
        bp_text = BLUEPRINT_2_FULL

    def test_part1(_):
        bp_text = BLUEPRINT_2_PARTIAL_1

    def test_empty(_):
        bp_text = BLUEPRINT_2_EMPTY


class Test3:  # with PROMPT3  ##################################################

    corpus = PromptCorpusNode.parse(PROMPT3)

    def test_full(self):
        bp_text = BLUEPRINT_3_FULL

    def test_part1(_):
        bp_text = BLUEPRINT_3_PARTIAL_1

    def test_part2(_):
        bp_text = BLUEPRINT_3_PARTIAL_2

    def test_empty(_):
        bp_text = BLUEPRINT_3_EMPTY
