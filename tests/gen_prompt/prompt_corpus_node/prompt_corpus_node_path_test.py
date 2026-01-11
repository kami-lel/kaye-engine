"""
test .names_path
"""

from kaye.gen_prompt import PromptCorpusNode
from tests.gen_prompt.prompt_corpus_node.testees import (
    PROMPT1,
    PROMPT3,
)


class TestParse1:  # test using PROMPT1

    def test_root(self):
        tree = PromptCorpusNode.parse(PROMPT1)

        names = tree.path_of_names

        print(names)
        assert isinstance(names, tuple)
        assert names == tuple()

    def test_project(self):
        tree = PromptCorpusNode.parse(PROMPT1)
        project = tree.children[0]

        names = project.names_path

        print(names)
        assert names == ("Project Title",)

    def test_sub1(self):
        tree = PromptCorpusNode.parse(PROMPT1)
        project = tree.children[0]
        sub = project.children[0]

        names = sub.names_path

        print(names)
        assert names == ("Project Title", "Description")

    def test_sub2(self):
        tree = PromptCorpusNode.parse(PROMPT1)
        project = tree.children[0]
        sub = project.children[1]

        names = sub.names_path

        print(names)
        assert names == ("Project Title", "Installation")

    def test_sub3(self):
        tree = PromptCorpusNode.parse(PROMPT1)
        project = tree.children[0]
        sub = project.children[2]

        names = sub.names_path

        print(names)
        assert names == ("Project Title", "License")


class TestParse3:  # test using PROMPT3

    def test_intro(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        node = project.children[0]

        names = node.names_path

        print(names)
        assert names == ("Main Title", "Introduction")

    def test_intro_bg(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[0]
        node = parent.children[0]

        names = node.names_path

        print(names)
        assert names == ("Main Title", "Introduction", "Background")

    def test_intro_bg_mpt(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[0].children[0]
        node = parent.children[0]

        names = node.names_path

        print(names)
        assert names == (
            "Main Title",
            "Introduction",
            "Background",
            "Importance",
        )

    def test_intro_bg_mpt_obj(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[0].children[0].children[0]
        node = parent.children[0]

        names = node.names_path

        print(names)
        assert names == (
            "Main Title",
            "Introduction",
            "Background",
            "Importance",
            "Objective",
        )

    def test_met(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        node = project.children[1]

        names = node.names_path

        print(names)
        assert names == ("Main Title", "Methods")

    def test_met_dc(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[1]
        node = parent.children[0]

        names = node.names_path

        print(names)
        assert names == (
            "Main Title",
            "Methods",
            "Data Collection",
        )

    def test_met_dc_tu(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[1].children[0]
        node = parent.children[0]

        names = node.names_path

        print(names)
        assert names == (
            "Main Title",
            "Methods",
            "Data Collection",
            "Tools Used",
        )

    def test_met_dc_tu_fw(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        parent = project.children[1].children[0].children[0]
        node = parent.children[0]

        names = node.names_path

        print(names)
        assert names == (
            "Main Title",
            "Methods",
            "Data Collection",
            "Tools Used",
            "Future Work",
        )

    def test_concl(self):
        tree = PromptCorpusNode.parse(PROMPT3)
        project = tree.children[0]
        node = project.children[2]

        names = node.names_path

        print(names)
        assert names == ("Main Title", "Conclusion")
