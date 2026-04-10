__all__ = [
    "assert_sense_title1",
    "assert_sense_title2",
    "assert_diff_title",
    "assert_diff1",
    "assert_diff2",
    "assert_diff3",
    "assert_diff4",
    "assert_diff5",
    "assert_diff6",
    "assert_diff7",
    "assert_zero_diff1",
    "assert_zero_diff2",
    "assert_role_title",
    "assert_role1",
    "assert_role2",
    "assert_role3",
    "assert_role4",
    "assert_role5",
    "assert_role6",
    "assert_role7",
    "assert_empty_role1",
    "assert_empty_role2",
    "assert_empty_pls1",
    "assert_empty_pls2",
]

# helpers  #####################################################################


def assert_sense_title1(opt):
    assert opt.startswith("# Kaye Chat")


def assert_sense_title2(opt):
    assert "## sense" in opt


# diff  ========================================================================


def assert_diff_title(opt):
    assert "### sense difficulty" in opt


def assert_diff1(opt):
    assert "Provide a number between `1` (very easy)" in opt


def assert_diff2(opt):
    assert "Use these tasks as your **anchor point**" in opt


def assert_diff3(opt):
    assert "- `3` Correct a single typo or awkward word " in opt


def assert_diff4(opt):
    assert "- `50` Fix a misunderstanding caused by missing" in opt


def assert_diff5(opt):
    assert "- `75` Choose and apply an appropriate common" in opt


def assert_diff6(opt):
    assert "- `96` Integrate a standard external source" in opt


def assert_diff7(opt):
    assert "- `100` Refactor a messy, ambiguous" in opt


# zero diff ====================================================================


def assert_zero_diff1(opt):
    assert "### zero difficulty" in opt


def assert_zero_diff2(opt):
    assert "`difficulty` must be `0`" in opt


# role  ========================================================================


def assert_role_title(opt):
    assert "### sense role" in opt


def assert_role1(opt):
    assert "select exactly one role. choose the" in opt


def assert_role2(opt):
    assert "- `art`: when the user gives you **a visual idea for" in opt


def assert_role3(opt):
    assert "- `changelog`: when the user gives you **changelog or" in opt


def assert_role4(opt):
    assert "- `chat`: when the user gives you a **general question" in opt


def assert_role5(opt):
    assert "- `coder`: when the user gives you **code or" in opt


def assert_role6(opt):
    assert "- `librarian`: when the user gives you **a text to read" in opt


def assert_role7(opt):
    assert "- `secretary`: when the user gives you" in opt


# TODO assert all roles

# empty role  ==================================================================


def assert_empty_role1(opt):
    assert "### empty role" in opt


def assert_empty_role2(opt):
    assert "`role` must be empty string" in opt


# empty PLs  ===================================================================


def assert_empty_pls1(opt):
    assert "### empty programming_languages" in opt


def assert_empty_pls2(opt):
    assert "`programming_languages` must be empty string" in opt
