import copy


import pytest


from kaye.gen_prompt.today_node import TodayNode
from kaye.gen_prompt.prompt_blueprint import PromptBlueprint


@pytest.fixture(scope="session")
def dynamic_nodes_testee1(corpus_testee3):
    corpus = copy.deepcopy(corpus_testee3)
    text = ""  # TODO TODO
    return PromptBlueprint.parse(text, corpus_override=corpus)
