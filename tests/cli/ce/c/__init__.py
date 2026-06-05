import subprocess


def prepare_local_config_folder(tmp_path_factory, command, folder_name):
    config_folder = tmp_path_factory.mktemp(folder_name)

    # Execute continue export command with folder path
    cmd = command + str(config_folder)
    subprocess.run(cmd, shell=True, check=True)

    rules_folder = config_folder / "rules"

    return config_folder, rules_folder


RULE_FILES = [
    "abbr-currency_symbol.md",
    "abbr-language_code.md",
    "abbr-prefix.md",
    "abbr-programming_language_code.md",
    "abbr-starts_with-a.md",
    "abbr-starts_with-b.md",
    "abbr-starts_with-c.md",
    "abbr-starts_with-d.md",
    "abbr-starts_with-digits.md",
    "abbr-starts_with-e.md",
    "abbr-starts_with-f.md",
    "abbr-starts_with-g.md",
    "abbr-starts_with-h.md",
    "abbr-starts_with-i.md",
    "abbr-starts_with-k.md",
    "abbr-starts_with-l.md",
    "abbr-starts_with-m.md",
    "abbr-starts_with-n.md",
    "abbr-starts_with-o.md",
    "abbr-starts_with-other.md",
    "abbr-starts_with-p.md",
    "abbr-starts_with-q.md",
    "abbr-starts_with-r.md",
    "abbr-starts_with-s.md",
    "abbr-starts_with-t.md",
    "abbr-starts_with-u.md",
    "abbr-starts_with-v.md",
    "abbr-starts_with-w.md",
    "abbr-starts_with-x.md",
    "abbr-starts_with-y.md",
    "abbr-suffix.md",
    "abbr-symbol.md",
    "abbr-unit_of_measure.md",
    "annotation_marker_blueprint.md",
    "chat_blueprint.md",
    "coder_bash_blueprint.md",
    "coder_blueprint.md",
    "coder_c_blueprint.md",
    "coder_changelog_blueprint.md",
    "coder_cpp_blueprint.md",
    "coder_csharp_blueprint.md",
    "coder_gdscript_blueprint.md",
    "coder_html_blueprint.md",
    "coder_js_ts_blueprint.md",
    "coder_project_blueprint.md",
    "coder_py_blueprint.md",
    "coder_py_docstring_blueprint.md",
    "coder_py_testing_blueprint.md",
    "coder_u3d_blueprint.md",
    "coder_ue_blueprint.md",
    "continue_behavior_blueprint.md",
    "date_time_blueprint.md",
    "number_unit_blueprint.md",
    "style_blueprint.md",
]
