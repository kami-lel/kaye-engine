# helpers  #####################################################################


def _assert_empty_role1(opt):
    assert "### empty role" in opt


def _assert_empty_role2(opt):
    assert "`role` must be empty string" in opt


def _assert_empty_pls1(opt):
    assert "### empty programming_languages" in opt


def _assert_empty_pls2(opt):
    assert "`programming_languages` must be empty string" in opt
