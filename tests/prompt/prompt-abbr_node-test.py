import copy


import pytest


from kaye.gen_prompt.abbr_nodes import AbbrNode


# pytest fixtures  #############################################################
@pytest.fixture(scope="session")
def local_corpus_testee1(corpus_testee1):
    return copy.deepcopy(corpus_testee1)


@pytest.fixture(scope="session")
def testee1(local_corpus_testee1):
    return AbbrNode(local_corpus_testee1)


class TestInit:  ###############################################################

    def test1(_, testee1, local_corpus_testee1):
        assert testee1.parent is local_corpus_testee1
        assert testee1.name == "Abbreviations"
        assert testee1.id == "{Abbreviations}"

    def test_preview1(_, local_corpus_testee1):
        opt = local_corpus_testee1.generate_prompt_tree_preview(
            content_preview_lines=0
        )
        print(opt)
        assert opt == """○
├── Project Title
│   ├── Description
│   ├── Installation
│   └── License
└── Abbreviations"""


class TestCopy:  ###############################################################

    def test_copy1(_, local_corpus_testee1, testee1):
        copied = copy.copy(testee1)

        assert isinstance(copied, AbbrNode)
        assert copied.name == "Abbreviations"
        assert copied.parent is local_corpus_testee1

    def test_deep_copy1(_, local_corpus_testee1, testee1):
        copied = copy.deepcopy(testee1)

        assert isinstance(copied, AbbrNode)
        assert copied.name == "Abbreviations"
        assert copied.parent is local_corpus_testee1


class TestContentLines:  #######################################################

    def test1(_):
        pass  # Todo abbr node functionality test
