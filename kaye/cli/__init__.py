"""
Kaye Python CLI
"""

from kaye.prompt.blueprint.embedded_blueprints import *


# blueprints exported by continue export & skill export
EXPORTABLE_BLUEPRINTS = [
    date_time_blueprint,
    number_unit_blueprint,
    triage_tags_blueprint,
    project_structure_blueprint,
    project_readme_blueprint,
    project_changelog_blueprint,
    project_agents_blueprint,
    project_semantic_versioning_blueprint,
    coder_blueprint,
    coder_bash_blueprint,
    coder_c_blueprint,
    coder_cpp_blueprint,
    coder_ue_blueprint,
    coder_csharp_blueprint,
    coder_u3d_blueprint,
    coder_gdscript_blueprint,
    coder_html_blueprint,
    coder_js_ts_blueprint,
    coder_py_blueprint,
    coder_py_docstring_blueprint,
    coder_py_testing_blueprint,
    style_title_case_blueprint,
    style_commentary_case_blueprint,
    style_briefness_blueprint,
    style_good_writing_blueprint,
    prompt_writer_blueprint,
    description_writer_blueprint,
    ipa_blueprint,
    role_art_tutor_blueprint,
    role_assistant_barista_blueprint,
    role_deutschlehrer_blueprint,
    role_editor_blueprint,
    role_librarian_blueprint,
    role_secretary_blueprint,
    role_tarot_reader_blueprint,
]
