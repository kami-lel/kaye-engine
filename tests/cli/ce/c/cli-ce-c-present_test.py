"""
cli-ce-c-present_test.py

Unit Tests (using pytest) for:

Python CLI command ``continue`` create all entries
"""

# Pytest unit tests  ###########################################################


class TestMain:  # =============================================================

    def test_abbr_currency_symbol(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-currency_symbol.md").exists()

    def test_abbr_language_code(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-language_code.md").exists()

    def test_abbr_prefix(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-prefix.md").exists()

    def test_abbr_programming_language_code(_, testee_rules_folder):
        assert (
            testee_rules_folder / "abbr-programming_language_code.md"
        ).exists()

    def test_abbr_starts_with_a(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-a.md").exists()

    def test_abbr_starts_with_b(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-b.md").exists()

    def test_abbr_starts_with_c(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-c.md").exists()

    def test_abbr_starts_with_d(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-d.md").exists()

    def test_abbr_starts_with_digits(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-digits.md").exists()

    def test_abbr_starts_with_e(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-e.md").exists()

    def test_abbr_starts_with_f(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-f.md").exists()

    def test_abbr_starts_with_g(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-g.md").exists()

    def test_abbr_starts_with_h(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-h.md").exists()

    def test_abbr_starts_with_i(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-i.md").exists()

    def test_abbr_starts_with_k(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-k.md").exists()

    def test_abbr_starts_with_l(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-l.md").exists()

    def test_abbr_starts_with_m(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-m.md").exists()

    def test_abbr_starts_with_n(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-n.md").exists()

    def test_abbr_starts_with_o(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-o.md").exists()

    def test_abbr_starts_with_other(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-other.md").exists()

    def test_abbr_starts_with_p(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-p.md").exists()

    def test_abbr_starts_with_q(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-q.md").exists()

    def test_abbr_starts_with_r(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-r.md").exists()

    def test_abbr_starts_with_s(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-s.md").exists()

    def test_abbr_starts_with_t(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-t.md").exists()

    def test_abbr_starts_with_u(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-u.md").exists()

    def test_abbr_starts_with_v(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-v.md").exists()

    def test_abbr_starts_with_w(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-w.md").exists()

    def test_abbr_starts_with_x(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-x.md").exists()

    def test_abbr_starts_with_y(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-starts_with-y.md").exists()

    def test_abbr_suffix(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-suffix.md").exists()

    def test_abbr_symbol(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-symbol.md").exists()

    def test_abbr_unit_of_measure(_, testee_rules_folder):
        assert (testee_rules_folder / "abbr-unit_of_measure.md").exists()

    def test_annotation_marker_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "annotation_marker_blueprint.md").exists()

    def test_chat_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "chat_blueprint.md").exists()

    def test_coder_bash_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "coder_bash_blueprint.md").exists()

    def test_coder_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "coder_blueprint.md").exists()

    def test_coder_c_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "coder_c_blueprint.md").exists()

    def test_coder_changelog_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "coder_changelog_blueprint.md").exists()

    def test_coder_cpp_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "coder_cpp_blueprint.md").exists()

    def test_coder_csharp_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "coder_csharp_blueprint.md").exists()

    def test_coder_gdscript_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "coder_gdscript_blueprint.md").exists()

    def test_coder_html_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "coder_html_blueprint.md").exists()

    def test_coder_js_ts_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "coder_js_ts_blueprint.md").exists()

    def test_coder_project_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "coder_project_blueprint.md").exists()

    def test_coder_py_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "coder_py_blueprint.md").exists()

    def test_coder_py_docstring_blueprint(_, testee_rules_folder):
        assert (
            testee_rules_folder / "coder_py_docstring_blueprint.md"
        ).exists()

    def test_coder_py_testing_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "coder_py_testing_blueprint.md").exists()

    def test_coder_u3d_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "coder_u3d_blueprint.md").exists()

    def test_coder_ue_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "coder_ue_blueprint.md").exists()

    def test_continue_behavior_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "continue_behavior_blueprint.md").exists()

    def test_date_time_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "date_time_blueprint.md").exists()

    def test_number_unit_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "number_unit_blueprint.md").exists()

    def test_style_blueprint(_, testee_rules_folder):
        assert (testee_rules_folder / "style_blueprint.md").exists()
