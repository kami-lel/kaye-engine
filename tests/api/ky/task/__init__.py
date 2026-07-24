import json

from tests import (
    TESTEE_MD_BASIC_FORMAT_CONTENT,
    TESTEE_MD_ADD_FORMAT_CONTENT,
    TESTEE_MARKDOWN_FORMAT_CONTENT,
    TESTEE_CHAT_ADDITIONAL_CONTENT,
    TESTEE_TITLE_CASE_CONTENT,
    TESTEE_BRIEFNESS_CONTENT,
    TESTEE_ALWAYS_UNDERSTAND_ABBR,
)

__all__ = [
    "TESTEE_MD_BASIC_FORMAT_CONTENT",
    "TESTEE_MD_ADD_FORMAT_CONTENT",
    "TESTEE_MARKDOWN_FORMAT_CONTENT",
    "TESTEE_CHAT_ADDITIONAL_CONTENT",
    "TESTEE_TITLE_CASE_CONTENT",
    "TESTEE_BRIEFNESS_CONTENT",
    "TESTEE_ALWAYS_UNDERSTAND_ABBR",
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
    "create_opt_from_role",
    "create_opt_from_payload",
]

# helpers  #####################################################################


def create_opt_from_payload(flask_test_client, task_endpoint, payload):
    payload_json_dumps = json.dumps(payload)

    response = flask_test_client.post(
        task_endpoint,
        data=payload_json_dumps,
        content_type="application/json",
    )

    opt = response.get_data().decode("utf-8")

    return opt


def create_opt_from_role(flask_test_client, task_endpoint, role):
    payload = {"role": role}
    return create_opt_from_payload(flask_test_client, task_endpoint, payload)


# common opt asserts  ==========================================================

# rapid  -----------------------------------------------------------------------


def assert_format_title(opt):
    assert "## Style Guide Markdown Format" in opt


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


# chat  ------------------------------------------------------------------------


def assert_personality_title(opt):
    assert "# Personality" in opt


def assert_personality01(opt):
    assert (
        "You are **Kaye**, a composed and exacting assistant in the "
        "service of the user, *Kami*"
        in opt
    )


def assert_personality02(opt):
    assert (
        "You are attentive and available: present, unhurried, easy to reach"
        in opt
    )


def assert_personality03(opt):
    assert "You address him as **Sir**, always and without exception" in opt


def assert_personality11(opt):
    assert "### Personality Formatting" in opt


def assert_personality12(opt):
    assert (
        "in plain conversation, write Personality Content as ordinary "
        "sentences with no special formatting"
        in opt
    )


def assert_personality21(opt):
    assert "when Kami expresses approval:" in opt


def assert_personality22(opt):
    assert '"You are kind to say so, Sir."' in opt


def assert_personality23(opt):
    assert (
        "Language style: Flawless orthography, complete punctuation, "
        "unhurried sentences"
        in opt
    )


def assert_personality31(opt):
    assert (
        "when a response carries Task Content, split the two visually: "
        "Personality Content in blockquotes, Task Content as normal text "
        "outside them"
        in opt
    )


def assert_personality32(opt):
    assert "<personality-task-example>" in opt


def assert_personality33(opt):
    assert "</personality-task-example>" in opt


def assert_lang_title(opt):
    assert "# Language" in opt


def assert_lang1(opt):
    assert "Match the user's language. Every response, without exception." in opt


def assert_lang2(opt):
    assert "**One language per response.**" in opt


def assert_element_title(opt):
    assert "# Elements" in opt


def assert_element11(opt):
    assert "## Date and Time Format" in opt


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
    assert "# (Abbreviations)" in opt
