"""
prompt_abbr_node_test.py

Unit Tests (using pytest) for:

- AbbrNode
"""

import pytest

from kaye.gen_prompt import PromptCorpusNode
from kaye.gen_prompt.abbr_nodes import AbbrNode

from tests.prompt import PROMPT1

tree = PromptCorpusNode.parse(PROMPT1)


class TestAbbrNode:

    node = AbbrNode(tree)

    def test_init(self):
        self.node.parent is tree
        self.node.name == "Abbreviations"
        self.node.id == "{Abbreviations}"

    def test_preview(self):
        opt = tree.generate_prompt_tree_preview(content_preview_lines=0)
        print(opt)
        assert opt == """○
├── Project Title
│   ├── Description
│   ├── Installation
│   └── License
└── Abbreviations"""

    # test content_lines  ------------------------------------------------------

    def test_fx1(self):
        query = "I am try.g to op.g on menu."

        lines = self.node.content_lines(query=query)

        print(lines)
        assert set(lines) == {"- op:operate,operation,operator", "- .g:-ing"}

    def test_fx2(self):
        query = (
            "The ind rev catalyzed a tectonic shift fr artisanal produc.n to"
            " mechanized manufacture, precipitating urbanization, the rise of"
            " factory labor, and new cls dynamics; & innovations in pub health,"
            " and pol repr. The period's cul ramifications incl the spread of"
            " literacy and reorder modn soc. This is really o.est."
        )

        lines = self.node.content_lines(query=query)

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
            "- pub:public;publish",
            "- ind:industry,industrial",
            "- in:inch",
            "- o.:over-",
            "- est.:estimate,estimation,estimated,estimating,estimatingly",
        }

    # TODO TODO multiple

    def test_caps1(self):
        query = "W it happens but mx and also AM"

        lines = self.node.content_lines(query=query)

        print(lines)
        assert set(lines) == {}  # BUG BUG

    def test_caps2(self):
        query = "w it happens but Mx and also am"

        lines = self.node.content_lines(query=query)

        print(lines)
        assert set(lines) == {}  # BUG BUG

    def test_emoji1(self):
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

        lines = self.node.content_lines(query=query)

        print(lines)
        assert set(lines) == {
            "- ⚠️:warning",
            "- ⚙️:settings,preferences",
            "- ☝:points/notice up;upward direction",
            "- 🚀:rapid,fast",
            "- ☜:points/notice left;left direction",
            "- 🛠️:tools",
            "- 🐞:debug",
            "- 🏁:finish",
            "- 🛑:error",
        }

    def test_unicode1(self):
        query = (
            "During the experiment, the temperature was carefully lowered ↓"
            " from 25℃ to 18℃ to observe the reaction rate changes. The"
            " solution's volume was reduced by ¼ to concentrate the reactants,"
            " ensuring more accurate results. After completing the checklist,"
            " the box marked with a ☒ indicated the step was successfully"
            " executed. These adjustments collectively contributed to the"
            " observed decrease ↓ in reaction time, confirming the hypothesis."
        )

        lines = self.node.content_lines(query=query)

        print(lines)
        assert set(lines) == {
            "- ℃:degree Celsius",
            "- ☒:selected with a cross",
            "- ↓:decrease,decrement",
            "- ¼:fraction one quarter",
            "- in:inch",
        }

    def test_empty1(self):
        query = "some content without abbreviation"

        lines = self.node.content_lines(query=query)
        print(lines)
        assert lines == []

    def test_err1(self):

        with pytest.raises(ValueError) as exec_info:
            self.node.content_lines()

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "must provide kwarg: query"
