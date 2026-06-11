"""
cli-ce-c-structure_test.py

Unit Tests (using pytest) for:

Python CLI command ``continue`` with creating correct structure
"""

from tests.cli.ce.c import RULE_FILES

# Pytest unit tests  ###########################################################


class TestMain:  # =============================================================

    def test_exits(_, testee_rules_folder):
        assert testee_rules_folder.exists()

    def test_is_dir(_, testee_rules_folder):
        assert testee_rules_folder.is_dir()


# HACK rm, test present in actual unit test files instead


class TestPresent:  # ==========================================================

    def test_by_loop(_, testee_rules_folder):
        for v in RULE_FILES:
            assert (testee_rules_folder / v).exists()

    def test_abbr_currency_symbol(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Currency Symbols.md").exists()

    def test_abbr_language_code(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Natural Language Codes.md").exists()

    def test_abbr_prefix(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Prefixes.md").exists()

    def test_abbr_programming_language_code(_, testee_rules_folder):
        assert (
            testee_rules_folder / "Abbr Programming Language Codes.md"
        ).exists()

    def test_abbr_single_character(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Single Character.md").exists()

    def test_abbr_emoji(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Emoji.md").exists()

    def test_abbr_starts_with_a(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with A.md").exists()

    def test_abbr_starts_with_b(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with B.md").exists()

    def test_abbr_starts_with_c(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with C.md").exists()

    def test_abbr_starts_with_d(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with D.md").exists()

    def test_abbr_starts_with_digits(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with Digits 0~9.md").exists()

    def test_abbr_starts_with_e(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with E.md").exists()

    def test_abbr_starts_with_f(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with F.md").exists()

    def test_abbr_starts_with_g(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with G.md").exists()

    def test_abbr_starts_with_h(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with H.md").exists()

    def test_abbr_starts_with_i(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with I.md").exists()

    def test_abbr_starts_with_k(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with K.md").exists()

    def test_abbr_starts_with_l(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with L.md").exists()

    def test_abbr_starts_with_m(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with M.md").exists()

    def test_abbr_starts_with_n(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with N.md").exists()

    def test_abbr_starts_with_o(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with O.md").exists()

    def test_abbr_starts_with_other(_, testee_rules_folder):
        assert (
            testee_rules_folder / "Abbr Starts with Non-Alphanumeric.md"
        ).exists()

    def test_abbr_starts_with_p(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with P.md").exists()

    def test_abbr_starts_with_q(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with Q.md").exists()

    def test_abbr_starts_with_r(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with R.md").exists()

    def test_abbr_starts_with_s(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with S.md").exists()

    def test_abbr_starts_with_t(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with T.md").exists()

    def test_abbr_starts_with_u(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with U.md").exists()

    def test_abbr_starts_with_v(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with V.md").exists()

    def test_abbr_starts_with_w(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with W.md").exists()

    def test_abbr_starts_with_x(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with X.md").exists()

    def test_abbr_starts_with_y(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Starts with Y.md").exists()

    def test_abbr_suffix(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Suffixes.md").exists()

    def test_abbr_symbol(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Symbols.md").exists()

    def test_abbr_unit_of_measure(_, testee_rules_folder):
        assert (testee_rules_folder / "Abbr Units of Measure.md").exists()

    def test_annotation_marker_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Annotation Markers.md").exists()

    def test_chat_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Chat.md").exists()

    def test_coder_bash_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Coder Bash.md").exists()

    def test_coder_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Kaye Peer Coder.md").exists()

    def test_coder_c_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Coder C.md").exists()

    def test_coder_changelog_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Project CHANGELOG Writer.md").exists()

    def test_coder_agents_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Project AGENTS Writer.md").exists()

    def test_coder_readme_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Project README Writer.md").exists()

    def test_coder_cpp_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Coder CPP.md").exists()

    def test_coder_csharp_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Coder C Sharp.md").exists()

    def test_coder_gdscript_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Coder GDScript.md").exists()

    def test_coder_html_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Coder HTML.md").exists()

    def test_coder_js_ts_blueprint(_, testee_rules_folder):
        assert (
            testee_rules_folder / "Coder JavaScript and TypeScript.md"
        ).exists()

    def test_coder_project_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Project Structure.md").exists()

    def test_coder_py_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Coder Python.md").exists()

    def test_coder_py_docstring_blueprint(_, testee_rules_folder):
        assert (
            testee_rules_folder / "Coder Python Docstring Style.md"
        ).exists()

    def test_coder_py_testing_blueprint(_, testee_rules_folder):
        assert (
            testee_rules_folder / "Coder Python Testing Guidelines.md"
        ).exists()

    def test_coder_u3d_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Coder Unity Engine.md").exists()

    def test_coder_ue_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Coder Unreal Engine.md").exists()

    def test_continue_behavior_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Continue Behavior.md").exists()

    def test_date_time_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Date and Time Format.md").exists()

    def test_number_unit_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Numerical Values with Units.md").exists()

    def test_style_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "Style Guide.md").exists()
