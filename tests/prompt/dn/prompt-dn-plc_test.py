"""
prompt-plc-test.py

Unit Tests (using pytest) for:

PLCNode
"""

import copy


import pytest


from kaye_engine.prompt.dynamic_nodes import PLCNode


# pytest fixtures  #############################################################
@pytest.fixture(scope="session")
def local_corpus_testee1(corpus_testee1):
    return copy.deepcopy(corpus_testee1)


@pytest.fixture(scope="session")
def testee1(local_corpus_testee1):
    return PLCNode(local_corpus_testee1)


class TestInit:  ###############################################################

    def test1(_, testee1, local_corpus_testee1):
        assert testee1.parent is local_corpus_testee1
        assert testee1.name == "(Programming Languages Code)"

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
└── (Programming Languages Code)"""


class TestCopy:  ###############################################################

    def test_copy1(_, testee1):
        copied = copy.copy(testee1)

        assert isinstance(copied, PLCNode)
        assert copied.name == "(Programming Languages Code)"
        assert copied.parent is None

    def test_deep_copy1(_, testee1):
        copied = copy.deepcopy(testee1)

        assert isinstance(copied, PLCNode)
        assert copied.name == "(Programming Languages Code)"
        assert copied.parent is None


class TestContentLines:  #######################################################

    def test1(_, testee1):
        opt = testee1.content_lines()
        print(opt)
        assert opt == [
            "- bash:Bash",
            "- c:C language",
            "- csharp:C Sharp",
            "- cpp:C++",
            "- css:CSS",
            "- gdscript:GDScript used by Godot Engine",
            "- html:HTML",
            "- js:JavaScript",
            "- py:Python",
            "- ts:TypeScript",
            "- u3d:Unity Engine code",
            "- ue:Unreal Engine code",
        ]
