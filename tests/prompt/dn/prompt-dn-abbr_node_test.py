"""
prompt-abbr_node-test.py

Unit Tests (using pytest) for: AbbrNode
"""

import copy


import pytest


from kaye.prompt.dynamic_nodes import AbbrNode


# fixtures data  ################################################################
_ALWAYS_UNDERSTAND_LINES = [
    "- abt:about",
    "- add.:additional,additionally,in addition",
    "- A:also",
    "- alt:alternative,alternatively",
    "- ~:and the others (non-people; eg a, b, ~; use ~~ when when ~ is"
    " ambiguous; eg a, b, ~~)",
    "- aot:another",
    "- answ:answer",
    "- a/:any",
    "- apch:approach",
    "- appr:appropriate,appropriately",
    "- R:are",
    "- asm:assume,assumed,assumption",
    "- bg:background",
    "- b.:bad",
    "- b4:before",
    "- gx:best",
    "- gg:better",
    "- B:but,however",
    "- Cx:can not,could not",
    "- C:can,could",
    "- chg:change",
    "- col:column",
    "- cpl:complete,completed,completion,completely,completeness",
    "- cond:condition,conditional",
    "- cf.:confer,compare",
    "- c.nt:connect,connection,connected",
    "- ctxt:context",
    "- cont:continue,continued,continuation",
    "- ctr:control",
    "- cor:correct,correction",
    "- cur:current,currently",
    "- d.c:decrease,decrement",
    "- def:define,definition,definite,definitive",
    "- dep:depend,dependent,dependence,dependency",
    "- dif:difference,different",
    "- diff:difficult,difficulty",
    "- do.:ditto,repetitive as above",
    "- ed:edit,edition,edited",
    "- mfa:emphasize,emphasis,emphatic",
    "- e/:every",
    "- e/o:everyone",
    "- e/t:everything",
    "- e/X:everytime",
    "- xcl:exclude,exclusion",
    "- xsi:exist,existence,there exists,existing",
    "- xpc:expect,expectation,expected",
    "- xpl:explain,explanation",
    "- vv:extreme,extremely",
    "- 4:for",
    "- fr:from",
    "- g.:good",
    "- grp:group,grouping",
    "- iff:if and only if",
    "- mpt:important,importance",
    "- mpv:improve,improvement",
    "- re:in the matter of,concerning,regarding",
    "- icl:include,inclusion",
    "- i.c:increase,increment",
    "- i.dep:independent,independence",
    "- iss:issue",
    "- lang:language",
    "- lx:least,fewest",
    "- ll:less,fewer",
    "- L:like,likely",
    "- ls:list",
    "- l.:little,few",
    "- mk:make",
    "- m.:many,much",
    "- mthd:method",
    "- mm:more",
    "- mx:most",
    "- mv:move",
    "- M:must",
    "- Mx:must not",
    "- nec:necessary",
    "- n/t:nothing",
    "- O:only",
    "- org:organize,organization",
    "- ot:other",
    "- pa:part,partial",
    "- pp:person,people,popular",
    "- pl:place,placement",
    "- pt:point",
    "- poss:possible,possibly",
    "- prev:previous",
    "- prob:probably,probability",
    "- ques:question",
    "- rand:random,randomize",
    "- rs:reason,reasoning",
    "- rl:relate",
    "- rlv:relevant,relative",
    "- rpt:repetition",
    "- rsch:research",
    "- rsrc:resource",
    "- rsp:respect,respective,respectively",
    "- crsp:correspond,corresponding",
    "- sep:separate",
    "- sl:should,shall",
    "- slx:should/shall not",
    "- sim.:similar",
    "- s/:some",
    "- stn:standard",
    "- st:state/status",
    "- succ:successful",
    "- |:such that",
    "- tk:take",
    "- T:than",
    "- tt:that,those",
    "- T:then",
    "- tf:therefore,causing,resulting",
    "- ts:this,these",
    "- X:time,times",
    "- 2:to",
    "- 2:too",
    "- ud:under",
    "- udsd:understand",
    "- upd:update",
    "- v.:very",
    "- W:while,when",
    "- bb:worse",
    "- bx:worst",
]


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
        assert testee1.name == "(Abbreviations)"

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
└── (Abbreviations)"""


class TestCopy:  ###############################################################

    def test_copy1(_, testee1):
        copied = copy.copy(testee1)

        assert isinstance(copied, AbbrNode)
        assert copied.name == "(Abbreviations)"
        assert copied.parent is None

    def test_deep_copy1(_, testee1):
        copied = copy.deepcopy(testee1)

        assert isinstance(copied, AbbrNode)
        assert copied.name == "(Abbreviations)"
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
            "- cls:class",
            "- cls:classic,classicism,classify,classical",
            "- pub:public",
            "- pub:publish",
            "- ind:industry,industrial",
            "- in:inch",
            "- o.:over-",
            "- est.:estimate,estimation,estimated,estimating,estimatingly",
            "- s:state/status",
        }

    def test_fx3(_, testee1):
        query = (
            "This is some 5PM time and it was 5 a.m. "
            "But i spent $5 to buy a book to read para 5."
        )

        lines = testee1.content_lines(query=query)

        print(lines)

        assert set(lines) == {
            "- $:US Dollar (default)",
            "- a.m.:ante meridiem,before midday",
            "- para:paragraph",
            "- PM:post meridiem,after midday",
        }

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
            "- ☒:selected (checkbox with a cross)",
            "- ↓:decrease,decrement",
            "- ¼:fraction one quarter",
            "- in:inch",
            "- s:state/status",
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
        assert lines == _ALWAYS_UNDERSTAND_LINES

    def test_empty3(_, testee1):
        lines = testee1.content_lines()
        print(lines)
        assert lines == _ALWAYS_UNDERSTAND_LINES
