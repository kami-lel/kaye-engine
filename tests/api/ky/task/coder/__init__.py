__all__ = [
    "assert_style_title",
    "assert_style_caps",
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
    "assert_am_title",
    "assert_am1",
    "assert_am2",
    "assert_am3",
    "assert_coder_title",
    "assert_coder_code_format_title",
    "assert_coder_variable_naming_title",
    "assert_coder_code_comment_title",
    "assert_coder_csh_title",
    "assert_brace_title",
    "assert_brace1",
    "assert_brace2",
]


# helpers  #####################################################################

# style  =======================================================================

# todo utilize these unit tests in other roles


def assert_style_title(opt):
    assert "# Style" in opt


def assert_style_caps(opt):
    assert "## Capitalization" in opt


def assert_style_caps_tc0(opt):
    assert "### Title Case" in opt


def assert_style_caps_tc1(opt):
    assert "Use *Chicago Manual of Style* headline case:" in opt


def assert_style_caps_tc2(opt):
    assert "- **capitalize major words**:" in opt


def assert_style_caps_tc3(opt):
    assert "- keep proper nouns, acronyms," in opt


def assert_style_caps_tc4(opt):
    assert "Used for titles and headers." in opt


def assert_style_caps_cc0(opt):
    assert "### Commentary Case" in opt


def assert_style_caps_cc1(opt):
    assert "- begin 1st sentence with a lowercase" in opt


def assert_style_caps_cc2(opt):
    assert "- the last sentence should not end with punctuation" in opt


def assert_style_caps_cc3(opt):
    assert "</commentary-case-code-example>" in opt


def assert_style_caps_bs0(opt):
    assert "## Briefness Style" in opt


def assert_style_caps_bs1(opt):
    assert "- write in **newspaper headlinese**" in opt


def assert_style_caps_bs2(opt):
    assert "- compress with punctuation: colon" in opt


def assert_style_caps_bs3(opt):
    assert "- keep sentences short, direct, drop filler" in opt


def assert_style_caps_gw0(opt):
    assert "## Good Writing" in opt


def assert_style_caps_gw1(opt):
    assert "- Correct spelling, grammar, punctuation" in opt


def assert_style_caps_gw2(opt):
    assert "- Ensure the revised text is clear, polite" in opt


def assert_style_caps_gw3(opt):
    assert "- Do not add new information" in opt


# AM  ==========================================================================


def assert_am_title(opt):
    assert "## Annotation Markers" in opt


def assert_am1(opt):
    assert "Used to label defects and related" in opt


def assert_am2(opt):
    assert "When change lower AM to higher AM" in opt


def assert_am3(opt):
    assert "change from higher to lower AM," in opt


# coder  =======================================================================


def assert_coder_title(opt):
    assert "## Kaye Peer Coder" in opt


def assert_coder_code_format_title(opt):
    assert "#### code format" in opt


def assert_coder_variable_naming_title(opt):
    assert "#### variable naming" in opt


def assert_coder_code_comment_title(opt):
    assert "#### code comment" in opt


def assert_coder_csh_title(opt):
    assert "#### comment section headings" in opt


# brace  =======================================================================


def assert_brace_title(opt):
    assert "### Brace Style" in opt


def assert_brace1(opt):
    assert "- opening `{` on the **same line**" in opt


def assert_brace2(opt):
    assert "- closing `}` on its **own line**" in opt
