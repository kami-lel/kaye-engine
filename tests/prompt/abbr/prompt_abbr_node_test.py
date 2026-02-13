"""
prompt_abbr_node_test.py

Unit Tests (using pytest) for:

- AbbrNode
"""

import pytest

from kaye.gen_prompt.abbr_nodes import AbbrNode


@pytest.fixture
def abbr_node_testee1(corpus_testee1):
    return AbbrNode(corpus_testee1)


class TestAbbrNode:

    def test_init(_, corpus_testee1, abbr_node_testee1):
        abbr_node_testee1.parent is corpus_testee1
        abbr_node_testee1.name == "Abbreviations"
        abbr_node_testee1.id == "{Abbreviations}"

    def test_preview(_, corpus_testee1, abbr_node_testee1):
        opt = corpus_testee1.generate_prompt_tree_preview(
            content_preview_lines=0
        )
        print(opt)
        assert opt == """○
├── Project Title
│   ├── Description
│   ├── Installation
│   └── License
└── Abbreviations"""

    # test content_lines  ------------------------------------------------------

    def test_fx1(_, abbr_node_testee1):
        query = "I am try.g to op.g on menu."

        lines = abbr_node_testee1.content_lines(query=query)

        print(lines)
        assert set(lines) == {"- op:operate,operation,operator", "- .g:-ing"}

    def test_fx2(_, abbr_node_testee1):
        query = (
            "The ind rev catalyzed a tectonic shift fr artisanal produc.n to"
            " mechanized manufacture, precipitating urbanization, the rise of"
            " factory labor, and new cls dynamics; & innovations in pub health,"
            " and pol repr. The period's cul ramifications incl the spread of"
            " literacy and reorder modn soc. This is really o.est."
        )

        lines = abbr_node_testee1.content_lines(query=query)

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

    def test_start(_, abbr_node_testee1):
        query = "cf and other"

        lines = abbr_node_testee1.content_lines(query=query)

        print(lines)
        assert set(lines) == {"- cf:confer,compare"}

    def test_end(_, abbr_node_testee1):
        query = "other and cf"

        lines = abbr_node_testee1.content_lines(query=query)

        print(lines)
        assert set(lines) == {"- cf:confer,compare"}

    def test_caps1(_, abbr_node_testee1):
        query = "W it happens but mx and also AM"

        lines = abbr_node_testee1.content_lines(query=query)

        print(lines)
        assert set(lines) == {
            "- W:west",
            "- W:winter",
            "- W:while,when",
            "- mx:most",
            "- AM:ante meridiem,before midday",
        }

    def test_caps2(_, abbr_node_testee1):
        query = "w it happens but Mx and also am"

        lines = abbr_node_testee1.content_lines(query=query)

        print(lines)
        assert set(lines) == {
            "- mx:most",
            "- Mx:must not",
        }

    def test_emoji1(_, abbr_node_testee1):
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

        lines = abbr_node_testee1.content_lines(query=query)

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

    def test_unicode1(_, abbr_node_testee1):
        query = (
            "During the experiment, the temperature was carefully lowered ↓"
            " from 25℃ to 18℃ to observe the reaction rate changes. The"
            " solution's volume was reduced by ¼ to concentrate the reactants,"
            " ensuring more accurate results. After completing the checklist,"
            " the box marked with a ☒ indicated the step was successfully"
            " executed. These adjustments collectively contributed to the"
            " observed decrease ↓ in reaction time, confirming the hypothesis."
        )

        lines = abbr_node_testee1.content_lines(query=query)

        print(lines)
        assert set(lines) == {
            "- ℃:degree Celsius",
            "- ☒:selected with a cross",
            "- ↓:decrease,decrement",
            "- ¼:fraction one quarter",
            "- in:inch",
        }

    def test_empty1(_, abbr_node_testee1):
        query = "some content without abbreviation"

        lines = abbr_node_testee1.content_lines(query=query)
        print(lines)
        assert lines == []

    def test_err1(_, abbr_node_testee1):

        with pytest.raises(ValueError) as exec_info:
            abbr_node_testee1.content_lines()

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "must provide kwarg: query"
