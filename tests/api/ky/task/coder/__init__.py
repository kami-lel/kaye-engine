__all__ = [
    "assert_style_title",
    "assert_style_caps_tc0",
    "assert_style_caps_tc1",
    "assert_style_caps_tc2",
    "assert_style_caps_tc3",
    "assert_style_caps_tc4",
    "assert_style_caps_cc0",
    "assert_style_caps_cc1",
    "assert_style_caps_cc2",
    "assert_style_caps_cc3",
    "assert_style_caps_bs0",
    "assert_style_caps_bs1",
    "assert_style_caps_bs2",
    "assert_style_caps_bs3",
    "assert_style_caps_gw0",
    "assert_style_caps_gw1",
    "assert_style_caps_gw2",
    "assert_style_caps_gw3",
    "assert_coder_title",
    "assert_coder_code_format_title",
    "assert_coder_variable_naming_title",
    "assert_coder_code_comment_title",
    "assert_coder_csh_title",
    "assert_brace_title",
    "assert_brace1",
    "assert_brace2",
    "assert_coder_c_title",
    "assert_coder_c1",
    "assert_coder_cpp_title",
    "assert_coder_cpp1",
    "assert_js_ts00",
    "assert_js_ts01",
    "assert_js_ts11",
    "assert_js_ts12",
    "assert_js_ts21",
    "assert_js_ts22",
    "assert_js_ts23",
    "assert_js_ts24",
    "assert_cs0",
    "assert_cs1",
    "assert_py_title",
    "assert_py_intro",
    "assert_py_doc0",
    "assert_py_doc1",
    "assert_py_pytest0",
    "assert_py_pytest1",
    "assert_py_pytest2",
]


# helpers  #####################################################################

# style  =======================================================================


def assert_style_title(opt):
    assert "# Style" in opt


def assert_style_caps_tc0(opt):
    assert "## Style Guide Title Case" in opt


def assert_style_caps_tc1(opt):
    assert "Use *Chicago Manual of Style* headline case:" in opt


def assert_style_caps_tc2(opt):
    assert "- **capitalize major words**:" in opt


def assert_style_caps_tc3(opt):
    assert "- keep proper nouns, acronyms," in opt


def assert_style_caps_tc4(opt):
    assert "Used for **document title** and **section headings**." in opt


def assert_style_caps_cc0(opt):
    assert "## Style Guide Commentary Case" in opt


def assert_style_caps_cc1(opt):
    assert "- begin 1st sentence with a lowercase" in opt


def assert_style_caps_cc2(opt):
    assert "- the last sentence should not end with punctuation" in opt


def assert_style_caps_cc3(opt):
    assert "</commentary-case-code-example>" in opt


def assert_style_caps_bs0(opt):
    assert "## Style Guide Briefness Style" in opt


def assert_style_caps_bs1(opt):
    assert "- write in **newspaper headlinese**" in opt


def assert_style_caps_bs2(opt):
    assert "- compress with punctuation: colon" in opt


def assert_style_caps_bs3(opt):
    assert "- keep sentences short, direct, drop filler" in opt


def assert_style_caps_gw0(opt):
    assert "## Style Guide Good Writing" in opt


def assert_style_caps_gw1(opt):
    assert "- Correct spelling, grammar, punctuation" in opt


def assert_style_caps_gw2(opt):
    assert "- Ensure the revised text is clear, polite" in opt


def assert_style_caps_gw3(opt):
    assert "- Do not add new information" in opt


# TT (Triage Tags)  ==========================================================


def assert_tt_title(opt):
    assert "## Triage Tags" in opt


def assert_tt1(opt):
    assert "Used to label defects and related" in opt


def assert_tt2(opt):
    assert "Changing a Quiet/Steady TT to a louder tier" in opt


def assert_tt3(opt):
    assert "changing to a quieter tier" in opt


# coder  =======================================================================


def assert_coder_title(opt):
    assert "# Kaye Peer Coder" in opt


def assert_coder_code_format_title(opt):
    assert "### code format" in opt


def assert_coder_variable_naming_title(opt):
    assert "### variable naming" in opt


def assert_coder_code_comment_title(opt):
    assert "### code comment" in opt


def assert_coder_csh_title(opt):
    assert "### comment section headings" in opt


# brace  =======================================================================


def assert_brace_title(opt):
    assert "## Brace Style" in opt


def assert_brace1(opt):
    assert "- opening `{` on the **same line**" in opt


def assert_brace2(opt):
    assert "- closing `}` on its **own line**" in opt


# PLs  =========================================================================

# C  ***************************************************************************


def assert_coder_c_title(opt):
    assert "## Coder C" in opt


def assert_coder_c1(opt):
    assert "Use **C99** standard" in opt


# C++  *************************************************************************


def assert_coder_cpp_title(opt):
    assert "## Coder CPP" in opt


def assert_coder_cpp1(opt):
    assert "Use **C++17** standard" in opt


# ts & js  *********************************************************************


def assert_js_ts00(opt):
    assert "## Coder JavaScript and TypeScript" in opt


def assert_js_ts01(opt):
    assert "These standards are applicable exclusively" in opt


def assert_js_ts11(opt):
    assert "#### Naming Conventions" in opt


def assert_js_ts12(opt):
    assert "- Use **camelCase** for naming variables" in opt


def assert_js_ts21(opt):
    assert "### Documentation and Comments" in opt


def assert_js_ts22(opt):
    assert "- Ensure the code is accompanied by" in opt


def assert_js_ts23(opt):
    assert "*Example of JSDoc documentation:*" in opt


def assert_js_ts24(opt):
    assert "globalNS.method1 = function (a, b)" in opt


# c#  **************************************************************************


def assert_cs0(opt):
    assert "## Coder C Sharp" in opt


def assert_cs1(opt):
    assert "- Documentation: Use XML comments" in opt


# python  **********************************************************************


def assert_py_title(opt):
    assert "## Coder Python" in opt


def assert_py_intro(opt):
    assert "Adhere to the **PEP8** style guide," in opt


def assert_py_doc0(opt):
    assert "### Coder Python Docstring Style" in opt


def assert_py_doc1(opt):
    assert "The docstrings must be written using the" in opt


def assert_py_pytest0(opt):
    assert "### Coder Python Testing Guidelines" in opt


def assert_py_pytest1(opt):
    assert "This section pertains specifically to Python test code" in opt


def assert_py_pytest2(opt):
    assert "*Example of tests for the `add` function:*" in opt
