"""
prompt-sidecar_node_test.py

Unit Tests (using pytest) for:

- BlueprintDescriptorSidecars
"""

import pytest

from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode
from kaye_engine.prompt.sidecar_node import BlueprintDescriptorSidecars


@pytest.fixture
def plain_node():
    root = PromptCorpusNode("○", None, [])
    proj = PromptCorpusNode("Personality", root, [])
    return PromptCorpusNode(
        "Ria When to Use", proj, ["Use when summoning Ria."]
    )


# pytest  ######################################################################
class TestBlueprintDescriptorSidecars:

    def test_when_to_use_node_assignable_to_plain_node(_, plain_node):
        sidecars = BlueprintDescriptorSidecars()
        sidecars.when_to_use_node = plain_node

        assert sidecars.when_to_use == "Use when summoning Ria."

    def test_description_node_assignable_to_plain_node(_, plain_node):
        sidecars = BlueprintDescriptorSidecars()
        sidecars.description_node = plain_node

        assert sidecars.description == "Use when summoning Ria."
