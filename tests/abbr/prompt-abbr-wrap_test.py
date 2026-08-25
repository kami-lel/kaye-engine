"""
prompt_abbr_wrap_test.py

Unit Tests (using pytest) for: AbbrWarp
"""

from kaye_engine.abbr_collection import AbbrWrap


# .is_satisfied_wrap_rule  #####################################################
class TestRuleWord:  # =========================================================

    enum = AbbrWrap.WORD

    # true cases  **************************************************************
    def test_true1(self):
        ipt = (" ", " ")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true2(self):
        ipt = ("", " ")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true3(self):
        ipt = (" ", "")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true4(self):
        ipt = ("", "")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true5(self):
        ipt = ("", "!")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true6(self):
        ipt = ("", ":")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true7(self):
        ipt = (",", " ")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true8(self):
        ipt = ("\n", "")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true9(self):
        ipt = ("\t", " ")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    # false cases  *************************************************************
    def test_false1(self):
        ipt = ("a", "z")
        print(ipt)
        assert not self.enum.is_satisfied_wrap_rule(*ipt)

    def test_false2(self):
        ipt = ("a", "")
        print(ipt)
        assert not self.enum.is_satisfied_wrap_rule(*ipt)

    def test_false3(self):
        ipt = (" ", "z")
        print(ipt)
        assert not self.enum.is_satisfied_wrap_rule(*ipt)


class TestRulePrefix:  # =======================================================

    enum = AbbrWrap.PREFIX

    # true cases  **************************************************************
    def test_true1(self):
        ipt = (" ", "a")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true2(self):
        ipt = ("\t", "a")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    # false cases  *************************************************************
    def test_false1(self):
        ipt = ("", "")
        print(ipt)
        assert not self.enum.is_satisfied_wrap_rule(*ipt)

    def test_false2(self):
        ipt = (" ", "!")
        print(ipt)
        assert not self.enum.is_satisfied_wrap_rule(*ipt)


class TestRuleSuffix:  # =======================================================

    enum = AbbrWrap.SUFFIX

    # true cases  **************************************************************
    def test_true1(self):
        ipt = ("a", " ")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true2(self):
        ipt = ("a", "\n")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    # false cases  *************************************************************
    def test_false1(self):
        ipt = ("", "")
        print(ipt)
        assert not self.enum.is_satisfied_wrap_rule(*ipt)

    def test_false2(self):
        ipt = ("!", " ")
        print(ipt)
        assert not self.enum.is_satisfied_wrap_rule(*ipt)


class TestRuleTermDef:  # ======================================================

    enum = AbbrWrap.TERM_DEF

    # false cases  *************************************************************
    def test_false1(self):
        ipt = (" ", " ")
        print(ipt)
        assert not self.enum.is_satisfied_wrap_rule(*ipt)

    def test_false2(self):
        ipt = ("", "")
        print(ipt)
        assert not self.enum.is_satisfied_wrap_rule(*ipt)

    def test_false3(self):
        ipt = (",", " ")
        print(ipt)
        assert not self.enum.is_satisfied_wrap_rule(*ipt)

    def test_false4(self):
        ipt = ("\t", " ")
        print(ipt)
        assert not self.enum.is_satisfied_wrap_rule(*ipt)

    def test_false5(self):
        ipt = ("a", "z")
        print(ipt)
        assert not self.enum.is_satisfied_wrap_rule(*ipt)


class TestRuleSymbol:  # =======================================================

    enum = AbbrWrap.SYMBOL

    # true cases  **************************************************************
    def test_true1(self):
        ipt = (" ", " ")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true2(self):
        ipt = ("", " ")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true3(self):
        ipt = (" ", "")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true4(self):
        ipt = ("", "")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true5(self):
        ipt = ("", "!")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true6(self):
        ipt = ("", ":")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true7(self):
        ipt = (",", " ")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true8(self):
        ipt = ("\n", "")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    def test_true9(self):
        ipt = ("\t", " ")
        print(ipt)
        assert self.enum.is_satisfied_wrap_rule(*ipt)

    # false cases  *************************************************************
    def test_false1(self):
        ipt = ("a", "z")
        print(ipt)
        assert not self.enum.is_satisfied_wrap_rule(*ipt)

    def test_false2(self):
        ipt = ("a", "")
        print(ipt)
        assert not self.enum.is_satisfied_wrap_rule(*ipt)

    def test_false3(self):
        ipt = (" ", "z")
        print(ipt)
        assert not self.enum.is_satisfied_wrap_rule(*ipt)
