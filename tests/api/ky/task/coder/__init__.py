__all__ = [
    "assert_coder_title",
    "assert_coder_code_format_title",
    "assert_coder_variable_naming_title",
    "assert_coder_code_comment_title",
    "assert_coder_csh_title",
]


# helpers  #####################################################################


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
