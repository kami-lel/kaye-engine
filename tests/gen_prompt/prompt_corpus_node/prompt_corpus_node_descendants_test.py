"""
test .get_descendants_paths()
"""

# TODO


from kaye.gen_prompt import PromptCorpusNode
from tests.gen_prompt.prompt_corpus_node.testees import (
    PROMPT1,
    PROMPT2,
    PROMPT3,
)


class TestParse1:  # test using PROMPT1

    def test_root(self):
        node = PromptCorpusNode.parse(PROMPT1)

        descendants_paths = node.get_descendants_paths()

        print(descendants_paths)
        assert isinstance(descendants_paths, list)
        assert descendants_paths == [
            ["Project Title"],
            ["Project Title", "Description"],
            ["Project Title", "Installation"],
            ["Project Title", "License"],
        ]

    def test_leaf(self):
        tree = PromptCorpusNode.parse(PROMPT1)
        project = tree.children[0]
        node = project.children[0]

        descendants_paths = node.get_descendants_paths()

        print(descendants_paths)
        assert descendants_paths == []


# TODO prompt2
# TODO prompt3
