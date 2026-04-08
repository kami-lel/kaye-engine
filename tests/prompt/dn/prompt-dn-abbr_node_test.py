"""
prompt-abbr_node-test.py

Unit Tests (using pytest) for: AbbrNode
"""

import copy


import pytest


from kaye.prompt.abbr_nodes import AbbrNode


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
        assert testee1.name == "{Abbreviations}"

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
└── {Abbreviations}"""


class TestCopy:  ###############################################################

    def test_copy1(_, testee1):
        copied = copy.copy(testee1)

        assert isinstance(copied, AbbrNode)
        assert copied.name == "{Abbreviations}"
        assert copied.parent is None

    def test_deep_copy1(_, testee1):
        copied = copy.deepcopy(testee1)

        assert isinstance(copied, AbbrNode)
        assert copied.name == "{Abbreviations}"
        assert copied.parent is None


class TestContentLines:  #######################################################

    def test_fx1(_, testee1):
        query = "I am try.g to op.g on menu."

        lines = testee1.content_lines(query=query)

        print(lines)
        assert set(lines) == {"- op:operate,operation,operator", "- .g:-ing"}

    def test_fx2(_, testee1):
        query = (
            "The ind rev catalyzed a tectonic shift fr artisanal produc.n to"
            " mechanized manufacture, precipitating urbanization, the rise of"
            " factory labor, and new cls dynamics; & innovations in pub health,"
            " and pol repr. The period's cul ramifications incl the spread of"
            " literacy and reorder modn soc. This is really o.est."
        )

        lines = testee1.content_lines(query=query)

        print(lines)

        assert set(lines) == {
            "- modn:modern,modernization",
            "- &:and",
            "- pol:politic,politics,political",
            "- repr:representation",
            "- soc:society",
            "- cul:culture,cultural",
            "- rev:revolution",
            "- fr:from",
            "- cls:class,classic,classicism,classify,classical",
            "- pub:public",
            "- pub:publish",
            "- ind:industry,industrial",
            "- in:inch",
            "- o.:over-",
            "- est.:estimate,estimation,estimated,estimating,estimatingly",
        }

    def test_fx3(_, testee1):
        pass  # TODO test currency

    def test_start(_, testee1):
        query = "cf and other"

        lines = testee1.content_lines(query=query)

        print(lines)
        assert set(lines) == {"- cf:confer,compare"}

    def test_end(_, testee1):
        query = "other and cf"

        lines = testee1.content_lines(query=query)

        print(lines)
        assert set(lines) == {"- cf:confer,compare"}

    def test_caps1(_, testee1):
        query = "W it happens but mx and also AM"

        lines = testee1.content_lines(query=query)

        print(lines)
        assert set(lines) == {
            "- W:west",
            "- W:winter",
            "- W:while,when",
            "- mx:most",
            "- AM:ante meridiem,before midday",
        }

    def test_caps2(_, testee1):
        query = "w it happens but Mx and also am"

        lines = testee1.content_lines(query=query)

        print(lines)
        assert set(lines) == {
            "- mx:most",
            "- Mx:must not",
        }

    def test_emoji1(_, testee1):
        query = (
            "When configuring your new software, always remember to review the"
            " ⚙️ settings carefully before proceeding. ☜ Ignoring these"
            " preferences can lead to unexpected behavior and potential errors"
            " 🛑 that might disrupt your workflow. If you encounter any issues,"
            " use the 🛠️ tools provided for debugging 🐞 to isolate the problem"
            " swiftly. ☝ Also, pay close attention to any ⚠️ warnings during"
            " installation—they often signal critical steps you must not"
            " overlook. Once all checks are complete and the process reaches"
            " the 🏁 finish line, you can confidently launch your project with"
            " a sense of accomplishment. Remember, a well-organized setup today"
            " fuels a rapid 🚀 and smooth experience tomorrow."
        )

        lines = testee1.content_lines(query=query)

        print(lines)
        assert set(lines) == {
            "- ⚙️:settings,preferences",
            "- 🚀:rapid,fast",
            "- ⚠️:warning",
            "- 🐞:debug",
            "- 🛑:error",
            "- ☝:points/notice up,upward",
            "- 🛠️:tools",
            "- ☜:points/notice left,left direction",
            "- 🏁:finish",
        }

    def test_unicode1(_, testee1):
        query = (
            "During the experiment, the temperature was carefully lowered ↓"
            " from 25℃ to 18℃ to observe the reaction rate changes. The"
            " solution's volume was reduced by ¼ to concentrate the reactants,"
            " ensuring more accurate results. After completing the checklist,"
            " the box marked with a ☒ indicated the step was successfully"
            " executed. These adjustments collectively contributed to the"
            " observed decrease ↓ in reaction time, confirming the hypothesis."
        )

        lines = testee1.content_lines(query=query)

        print(lines)
        assert set(lines) == {
            "- ℃:degree Celsius",
            "- ☒:selected with a cross",
            "- ↓:decrease,decrement",
            "- ¼:fraction one quarter",
            "- in:inch",
        }

    def test_empty1(_, testee1):
        query = "some content without abbreviation"

        lines = testee1.content_lines(query=query)
        print(lines)
        assert lines == []

    def test_empty2(_, testee1):
        query = ""

        lines = testee1.content_lines(query=query)
        print(lines)
        assert lines == []

    def test_empty3(_, testee1):
        lines = testee1.content_lines()
        print(lines)
        assert lines == []
