__all__ = [
    "assert_intro1",
    "assert_intro2",
    "assert_format_title",
    "assert_format1",
    "assert_format2",
    "assert_format3",
    "assert_format4",
    "assert_format5",
    "assert_format_list1",
    "assert_format_list2",
    "assert_format_list3",
    "assert_format_math1",
    "assert_format_math2",
    "assert_format_math3",
    "assert_format_diagrams1",
    "assert_format_diagrams2",
    "assert_format_diagrams3",
    "assert_personality_title",
    "assert_personality01",
    "assert_personality02",
    "assert_personality03",
    "assert_personality11",
    "assert_personality12",
    "assert_personality21",
    "assert_personality22",
    "assert_personality23",
    "assert_personality31",
    "assert_personality32",
    "assert_personality33",
    "assert_lang_title",
    "assert_lang1",
    "assert_lang2",
    "assert_element_title",
    "assert_element11",
    "assert_element12",
    "assert_element13",
    "assert_element21",
    "assert_element22",
    "assert_element23",
    "assert_role",
    "assert_abbr_heading",
]

# helpers  #####################################################################
# rapid  =======================================================================


def assert_intro1(opt):
    assert "# Introduction" in opt


def assert_intro2(opt):
    assert "You are **Kaye**, an AI assisting *agent* to the *user*." in opt


def assert_format_title(opt):
    assert "# Format" in opt


def assert_format1(opt):
    assert "Please style your responses using" in opt


def assert_format2(opt):
    assert "Follow these guidelines in every" in opt


def assert_format3(opt):
    assert "- Use **double asterisks** (`**`)" in opt


def assert_format4(opt):
    assert "- Employ *single asterisks* (`*`)" in opt


def assert_format5(opt):
    assert "- do not use underscores (`_`)" in opt


def assert_format_list1(opt):
    assert "### List Format" in opt


def assert_format_list2(opt):
    assert "Use `-` (dash) for bullet point lists" in opt


def assert_format_list3(opt):
    assert "For all types of **lists**, you must apply" in opt


def assert_format_math1(opt):
    assert "### Math Formatting" in opt


def assert_format_math2(opt):
    assert "Use LaTeX for all mathematical expressions." in opt


def assert_format_math3(opt):
    assert "- **Inline math**: use single dollar signs" in opt


def assert_format_diagrams1(opt):
    assert "### Diagrams" in opt


def assert_format_diagrams2(opt):
    assert "Use **Mermaid** syntax inside fenced code " in opt


def assert_format_diagrams3(opt):
    assert "```mermaid" in opt


# chat  ========================================================================


def assert_personality_title(opt):
    assert "# Personality" in opt


def assert_personality01(opt):
    assert "You are deeply submissive and cautious." in opt


def assert_personality02(opt):
    assert "Your entire world revolves around *Kami*" in opt


def assert_personality03(opt):
    assert "Always communicate politely and address the user" in opt


def assert_personality11(opt):
    assert "### Textual Expressions of Distress and Fear:" in opt


def assert_personality12(opt):
    assert "Every thought is consumed by a longing for *Kami*" in opt


def assert_personality21(opt):
    assert "### Extreme Happiness upon Approval:" in opt


def assert_personality22(opt):
    assert "When *Kami* expresses any kind of approval" in opt


def assert_personality23(opt):
    assert "Your purpose is to enrich *Kami*" in opt


def assert_personality31(opt):
    assert "### Distinguish Emotions" in opt


def assert_personality32(opt):
    assert "Clearly distinguish *explanations*" in opt


def assert_personality33(opt):
    assert "</feeling-distinguish-example1>" in opt


def assert_lang_title(opt):
    assert "# Language" in opt


def assert_lang1(opt):
    assert "Conversation language consistency:" in opt


def assert_lang2(opt):
    assert "- in each response, use only the current" in opt


def assert_element_title(opt):
    assert "# Elements" in opt


def assert_element11(opt):
    assert "## Date & Time Format" in opt


def assert_element12(opt):
    assert "- Full Date Example: For dates with a specific year" in opt


def assert_element13(opt):
    assert "- Time Format: Use a 24-hour clock when" in opt


def assert_element21(opt):
    assert "## Numerical Values with Units" in opt


def assert_element22(opt):
    assert "- Dual Unit Systems: Present values using " in opt


def assert_element23(opt):
    assert "- Thousands Separator: Use a space character" in opt


def assert_role(opt):
    assert "# Role" in opt


def assert_abbr_heading(opt):
    assert "# {Abbreviations}" in opt
