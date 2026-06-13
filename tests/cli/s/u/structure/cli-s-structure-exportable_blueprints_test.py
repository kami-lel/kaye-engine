"""
cli-s-structure-exportable_blueprints_test.py

Unit tests for EXPORTABLE_BLUEPRINTS using SkillMDFileFrontmatterValidator.
"""

from tests.cli.s.u.structure import validate_blueprint
from kaye.cli import agent_blueprint
from kaye.prompt.embedded_blueprints import (
    annotation_marker_blueprint,
    chat_blueprint,
    coder_bash_blueprint,
    coder_blueprint,
    coder_c_blueprint,
    coder_cpp_blueprint,
    coder_csharp_blueprint,
    coder_gdscript_blueprint,
    coder_html_blueprint,
    coder_js_ts_blueprint,
    coder_py_blueprint,
    coder_py_docstring_blueprint,
    coder_py_testing_blueprint,
    coder_u3d_blueprint,
    coder_ue_blueprint,
    date_time_blueprint,
    number_unit_blueprint,
    project_agents_blueprint,
    project_changelog_blueprint,
    project_readme_blueprint,
    project_semantic_versioning_blueprint,
    project_structure_blueprint,
    style_briefness_blueprint,
    style_capitalization_blueprint,
    style_good_writing_blueprint,
)

# valid  #######################################################################


def test_chat():
    r = validate_blueprint(chat_blueprint)
    assert r.name == "chat"


def test_date_and_time_format():
    r = validate_blueprint(date_time_blueprint)
    assert r.name == "date-and-time-format"


def test_numerical_values_with_units():
    r = validate_blueprint(number_unit_blueprint)
    assert r.name == "numerical-values-with-units"


def test_annotation_markers():
    r = validate_blueprint(annotation_marker_blueprint)
    assert r.name == "annotation-markers"


def test_project_structure():
    r = validate_blueprint(project_structure_blueprint)
    assert r.name == "project-structure"


def test_project_readme_writer():
    r = validate_blueprint(project_readme_blueprint)
    assert r.name == "project-readme-writer"


def test_project_changelog_writer():
    r = validate_blueprint(project_changelog_blueprint)
    assert r.name == "project-changelog-writer"


def test_project_agents_writer():
    r = validate_blueprint(project_agents_blueprint)
    assert r.name == "project-agents-writer"


def test_project_semantic_versioning():
    r = validate_blueprint(project_semantic_versioning_blueprint)
    assert r.name == "project-semantic-versioning"


def test_kaye_peer_coder():
    r = validate_blueprint(coder_blueprint)
    assert r.name == "kaye-peer-coder"


def test_coder_bash():
    r = validate_blueprint(coder_bash_blueprint)
    assert r.name == "coder-bash"


def test_coder_c():
    r = validate_blueprint(coder_c_blueprint)
    assert r.name == "coder-c"


def test_coder_cpp():
    r = validate_blueprint(coder_cpp_blueprint)
    assert r.name == "coder-cpp"


def test_coder_unreal_engine():
    r = validate_blueprint(coder_ue_blueprint)
    assert r.name == "coder-unreal-engine"


def test_coder_c_sharp():
    r = validate_blueprint(coder_csharp_blueprint)
    assert r.name == "coder-c-sharp"


def test_coder_unity_engine():
    r = validate_blueprint(coder_u3d_blueprint)
    assert r.name == "coder-unity-engine"


def test_coder_gdscript():
    r = validate_blueprint(coder_gdscript_blueprint)
    assert r.name == "coder-gdscript"


def test_coder_python():
    r = validate_blueprint(coder_py_blueprint)
    assert r.name == "coder-python"


def test_coder_python_docstring_style():
    r = validate_blueprint(coder_py_docstring_blueprint)
    assert r.name == "coder-python-docstring-style"


def test_coder_python_testing_guidelines():
    r = validate_blueprint(coder_py_testing_blueprint)
    assert r.name == "coder-python-testing-guidelines"


def test_style_guide_capitalization():
    r = validate_blueprint(style_capitalization_blueprint)
    assert r.name == "style-guide-capitalization"


def test_style_guide_briefness_style():
    r = validate_blueprint(style_briefness_blueprint)
    assert r.name == "style-guide-briefness-style"


def test_style_guide_good_writing():
    r = validate_blueprint(style_good_writing_blueprint)
    assert r.name == "style-guide-good-writing"


def test_coder_html():
    r = validate_blueprint(coder_html_blueprint)
    assert r.name == "coder-html"


def test_coder_javascript_and_typescript():
    r = validate_blueprint(coder_js_ts_blueprint)
    assert r.name == "coder-javascript-and-typescript"


def test_agent_behavior():
    r = validate_blueprint(agent_blueprint)
    assert r.name == "agent-behavior"
