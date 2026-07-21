"""
prompt-usable_test.py

Unit Tests (using pytest) for:

- UsableAbbrNode
"""

import copy


import pytest


from kaye.prompt.dynamic_nodes import UsableAbbrNode


# pytest fixtures  #############################################################
@pytest.fixture(scope="session")
def local_corpus_testee1(corpus_testee1):
    return copy.deepcopy(corpus_testee1)


@pytest.fixture(scope="session")
def testee1(local_corpus_testee1):
    return UsableAbbrNode(local_corpus_testee1)


class TestInit:  ###############################################################

    def test1(_, testee1, local_corpus_testee1):
        assert testee1.parent is local_corpus_testee1
        assert testee1.name == "(Usable Abbreviations)"

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
└── (Usable Abbreviations)"""


class TestCopy:  ###############################################################

    def test_copy1(_, testee1):
        copied = copy.copy(testee1)

        assert isinstance(copied, UsableAbbrNode)
        assert copied.name == "(Usable Abbreviations)"
        assert copied.parent is None

    def test_deep_copy1(_, testee1):
        copied = copy.deepcopy(testee1)

        assert isinstance(copied, UsableAbbrNode)
        assert copied.name == "(Usable Abbreviations)"
        assert copied.parent is None


class TestContentLines:  #######################################################

    def test1(_, testee1):
        opt = testee1.content_lines()
        print(opt)
        assert opt == [
            "- vs.:against",
            "- &:and",
            "- ~:and the others (non-people; eg a, b, ~; use ~~ when when ~ is"
            " ambiguous; eg a, b, ~~)",
            "- ⇐:because,caused by,result of",
            "- b/c:because,caused by,result of",
            "- ←:become/change/transform from",
            "- →:become/change/transform into",
            "- b/t:between",
            "- cf.:confer,compare",
            "- ↓:decrease,decrement",
            "- 〃:ditto,repetitive as above",
            "- =:equal,equality,equivalent,equivalence",
            "- e.g.:for example,for instance",
            "- >:greater than",
            "- ≥:greater than or equal to",
            "- h:hour",
            "- hr:hour (use when h is ambagious)",
            "- iff:if and only if",
            "- re:in the matter of,concerning,regarding",
            "- ↑:increase,increment",
            "- <:less than",
            "- ≤:less than or equal to",
            "- math:mathematics,mathematical",
            "- max:maximum,maximize,maximization",
            "- min:minimum,minimize,minimization",
            "- min:minute",
            "- misc.:miscellaneous",
            "- ×:multiply,multiplication,multiplier",
            "- n/a:not applicable",
            "- ≠:not equal",
            "- №:number",
            "- \\:of",
            "- /:or",
            "- p.s.:post scriptum,after what has been written,post script",
            "- ~:range (eg 1~5, a~f, ii~iv)",
            "- s:second",
            "- sec:second (use when s is ambagious)",
            "- ☑:selected (checkbox with a tick)",
            "- i.e.:that is,in other words",
            "- ⇒:therefore,causing,resulting",
            "- ☐:unselected (empty checkbox)",
            "- ※:which see,reference to",
            "- q.v.:which see,reference to (use qq.v. for multiple references)",
            "- w/:with",
            "- w/i:within",
            "- w/o:without",
        ]
