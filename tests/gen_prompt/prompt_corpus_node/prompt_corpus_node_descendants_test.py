"""
test .get_descendants_paths()
"""

from kaye.gen_prompt import PromptCorpusNode
from tests.gen_prompt.prompt_corpus_node.testees import (
    PROMPT1,
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


class TestParse3:  # test using PROMPT3

    def test_root(self):
        node = PromptCorpusNode.parse(PROMPT3)

        descendants_paths = node.get_descendants_paths()

        print(descendants_paths)
        assert isinstance(descendants_paths, list)
        assert descendants_paths == [
            ["Main Title"],
            ["Main Title", "Introduction"],
            ["Main Title", "Introduction", "Background"],
            ["Main Title", "Introduction", "Background", "Importance"],
            [
                "Main Title",
                "Introduction",
                "Background",
                "Importance",
                "Objective",
            ],
            ["Main Title", "Methods"],
            ["Main Title", "Methods", "Data Collection"],
            ["Main Title", "Methods", "Data Collection", "Tools Used"],
            [
                "Main Title",
                "Methods",
                "Data Collection",
                "Tools Used",
                "Future Work",
            ],
            ["Main Title", "Conclusion"],
        ]

    def test_node1(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        main_title = tree.children[0]
        node = main_title.children[0]

        descendants_paths = node.get_descendants_paths()

        print(descendants_paths)
        assert descendants_paths == [
            ["Main Title", "Introduction", "Background"],
            ["Main Title", "Introduction", "Background", "Importance"],
            [
                "Main Title",
                "Introduction",
                "Background",
                "Importance",
                "Objective",
            ],
        ]

    def test_node2(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        main_title = tree.children[0]
        node = main_title.children[1]

        descendants_paths = node.get_descendants_paths()

        print(descendants_paths)
        assert descendants_paths == [
            ["Main Title", "Methods", "Data Collection"],
            ["Main Title", "Methods", "Data Collection", "Tools Used"],
            [
                "Main Title",
                "Methods",
                "Data Collection",
                "Tools Used",
                "Future Work",
            ],
        ]

    def test_leaf(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        parent = tree.children[0].children[0].children[0].children[0]
        node = parent.children[0]

        descendants_paths = node.get_descendants_paths()

        print(descendants_paths)
        assert descendants_paths == []
