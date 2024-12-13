"""
test for function get_prompt
"""

PROMPT_FULL_FILE_PATH = '../../kaye/prompt_full.md'

from os.path import abspath, join, dirname

import pytest

from kaye.get_prompt import get_prompt
from kaye.get_prompt.prompt_tree_node import PromptTreeNode


def test_prompt_full():
    prompt_name = 'full'

    opt = get_prompt(prompt_name)

    # create a full prompt w/o repeating lines
    file_path = abspath(join(dirname(__file__), PROMPT_FULL_FILE_PATH))
    with open(file_path, 'r') as file:
        lines = file.read().split('\n')
        clean_lines = PromptTreeNode._init_lines_cleanup(lines)
        content = '\n'.join(l for l in clean_lines)

        assert content in opt



def test_err():
    prompt_name = '???'

    with pytest.raises(ValueError) as ei:
        get_prompt(prompt_name)

    assert str(ei.value) == "'???' of arg prompt_name not recognized"
