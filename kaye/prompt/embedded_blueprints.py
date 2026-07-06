"""
embedded_blueprints.py

common blueprints creations
"""

# pylint: disable=invalid-name

from kaye.prompt.prompt_blueprint import PromptBlueprint

__all__ = (
    "rapid_blueprint",
    "chat_blueprint",
    "date_time_blueprint",
    "number_unit_blueprint",
    "style_blueprint",
    "coder_blueprint",
    "project_structure_blueprint",
    "project_readme_blueprint",
    "project_changelog_blueprint",
    "project_agents_blueprint",
    "project_semantic_versioning_blueprint",
    "coder_bash_blueprint",
    "coder_c_blueprint",
    "coder_cpp_blueprint",
    "coder_ue_blueprint",
    "coder_csharp_blueprint",
    "coder_u3d_blueprint",
    "coder_gdscript_blueprint",
    "coder_html_blueprint",
    "coder_js_ts_blueprint",
    "coder_py_blueprint",
    "coder_py_docstring_blueprint",
    "coder_py_testing_blueprint",
    "triage_tags_blueprint",
    "style_title_case_blueprint",
    "style_commentary_case_blueprint",
    "style_briefness_blueprint",
    "style_good_writing_blueprint",
    "prompt_writer_blueprint",
    "description_writer_blueprint",
    "ipa_blueprint",
    "role_art_tutor_blueprint",
    "role_assistant_barista_blueprint",
    "role_deutschlehrer_blueprint",
    "role_editor_blueprint",
    "role_librarian_blueprint",
    "role_secretary_blueprint",
    "role_tarot_reader_blueprint",
)


# blueprints  ##################################################################
# (in corpus, but not as part of the content lines)


# Rapid
rapid_blueprint = PromptBlueprint.parse("""    ○
[x] ├── Introduction
[x] └── Style Guide
[x]     └── Style Guide Markdown Format
[x]         └── Additional Markdown Format""")
rapid_blueprint.display_name = "Rapid"
rapid_blueprint.sidecar.description = (
    "quick, mechanical text or data tasks with no persona or role"
)


# Chat
chat_blueprint = PromptBlueprint.parse("""    ○
[x] ├── Introduction
[x] ├── Personality
[x] ├── Language
[x] └── Style Guide
[x]     ├── Style Guide Markdown Format
[x]     │   └── Additional Markdown Format
[x]     └── Style Guide Commentary Case""")
chat_blueprint.display_name = "Chat"
chat_blueprint.sidecar.description = (
    "default for general conversation with full Kaye persona and role"
)


# Date and Time Format
date_time_blueprint = PromptBlueprint.create_from_node(
    "Date and Time Format", recursively=True
)

_corpus = date_time_blueprint.corpus


# Numerical Values with Units
number_unit_blueprint = PromptBlueprint.create_from_node(
    "Numerical Values with Units"
)


# Triage Tags
triage_tags_blueprint = PromptBlueprint.create_from_node(
    _corpus["Elements"]["Triage Tags"], recursively=True
)


# coder  =======================================================================

_kyc_node = _corpus["Kaye Peer Coder"]

# Coder
coder_blueprint = (
    PromptBlueprint.create_from_node(_kyc_node) | triage_tags_blueprint
)
coder_blueprint.display_name = "Kaye Peer Coder"


# Coder Bash
coder_bash_blueprint = PromptBlueprint.create_from_node(_kyc_node["Coder Bash"])


# Coder C
coder_c_blueprint = PromptBlueprint.create_from_node(_kyc_node["Coder C"])
coder_c_blueprint.checkmark(_kyc_node["Brace Style"])


# Coder C++
coder_cpp_blueprint = PromptBlueprint.create_from_node(_kyc_node["Coder CPP"])
PromptBlueprint.create_empty_blueprint()
coder_cpp_blueprint.checkmark(_kyc_node["Coder C"])
coder_cpp_blueprint.checkmark(_kyc_node["Brace Style"])


# Coder Unreal Engine
coder_ue_blueprint = PromptBlueprint.create_empty_blueprint()
coder_ue_blueprint = PromptBlueprint.create_from_node(
    _kyc_node["Coder Unreal Engine"]
)
coder_ue_blueprint.checkmark(_kyc_node["Coder C"])
coder_ue_blueprint.checkmark(_kyc_node["Coder CPP"])
coder_ue_blueprint.checkmark(_kyc_node["Brace Style"])


# Coder C Sharp
coder_csharp_blueprint = PromptBlueprint.create_from_node(
    _kyc_node["Coder C Sharp"]
)
coder_csharp_blueprint.checkmark(_kyc_node["Brace Style"])


# Coder Unity
coder_u3d_blueprint = PromptBlueprint.create_from_node(
    _kyc_node["Coder Unity Engine"], recursively=True
)
coder_u3d_blueprint.checkmark(_kyc_node["Coder C Sharp"])
coder_u3d_blueprint.checkmark(_kyc_node["Brace Style"])


# Coder GDScript
coder_gdscript_blueprint = PromptBlueprint.create_from_node(
    _kyc_node["Coder GDScript"]
)


# Coder HTML
coder_html_blueprint = PromptBlueprint.create_from_node(_kyc_node["Coder HTML"])


# Coder JavaScript and TypeScript
coder_js_ts_blueprint = PromptBlueprint.create_from_node(
    _kyc_node["Coder JavaScript and TypeScript"], recursively=True
)
coder_js_ts_blueprint.checkmark(_kyc_node["Brace Style"])


# Python  ----------------------------------------------------------------------
# Coder Python
coder_py_blueprint = PromptBlueprint.create_from_node(_kyc_node["Coder Python"])

# Coder Python Docstring
coder_py_docstring_blueprint = PromptBlueprint.create_from_node(
    _kyc_node["Coder Python"]["Coder Python Docstring Style"]
)


# Coder Python Testing
coder_py_testing_blueprint = PromptBlueprint.create_from_node(
    _kyc_node["Coder Python"]["Coder Python Testing Guidelines"]
)


# Project  =====================================================================

_proj_node = _corpus["Projects"]

project_structure_blueprint = PromptBlueprint.create_from_node(
    _proj_node["Project Structure"]
)

# Project README Writer
project_readme_blueprint = PromptBlueprint.create_from_node(
    _proj_node["Project README Writer"]
)

# Project CHANGELOG Writer
project_changelog_blueprint = PromptBlueprint.create_from_node(
    _proj_node["Project CHANGELOG Writer"], recursively=True
)


# Project AGENTS Writer
project_agents_blueprint = PromptBlueprint.create_from_node(
    _proj_node["Project AGENTS Writer"]
)

# Project Semantic Versioning
project_semantic_versioning_blueprint = PromptBlueprint.create_from_node(
    _proj_node["Project Semantic Versioning"]
)


# Style Guide  =================================================================

_style_node = _corpus["Style Guide"]


style_blueprint = PromptBlueprint.create_from_node(
    _style_node, recursively=True
)


style_title_case_blueprint = PromptBlueprint.create_from_node(
    _style_node["Style Guide Title Case"]
)

style_commentary_case_blueprint = PromptBlueprint.create_from_node(
    _style_node["Style Guide Commentary Case"]
)

style_briefness_blueprint = PromptBlueprint.create_from_node(
    _style_node["Style Guide Briefness Style"]
)

style_good_writing_blueprint = PromptBlueprint.create_from_node(
    _style_node["Style Guide Good Writing"]
)


# Prompt Engineering  ==========================================================

_prompt_engineer_node = _corpus["Prompt Engineering"]

prompt_writer_blueprint = PromptBlueprint.create_from_node(
    _prompt_engineer_node["Prompt Writer"], recursively=True
)

description_writer_blueprint = PromptBlueprint.create_from_node(
    _prompt_engineer_node["Skill Description Writer"], recursively=True
)


# International Phonetic Alphabet  ============================================

ipa_blueprint = PromptBlueprint.create_from_node(
    _corpus["Elements"]["International Phonetic Alphabet"]
)


# Roles  =======================================================================

_role_node = _corpus["Role"]

role_art_tutor_blueprint = PromptBlueprint.create_from_node(
    _role_node["Art Tutor"]
)

role_assistant_barista_blueprint = PromptBlueprint.create_from_node(
    _role_node["Assistant Barista"], recursively=True
)

role_deutschlehrer_blueprint = PromptBlueprint.create_from_node(
    _role_node["Deutschlehrer"]
)

role_editor_blueprint = PromptBlueprint.create_from_node(_role_node["Editor"])

role_librarian_blueprint = PromptBlueprint.create_from_node(
    _role_node["Librarian"], recursively=True
)

role_secretary_blueprint = PromptBlueprint.create_from_node(
    _role_node["Secretary"]
)

role_tarot_reader_blueprint = PromptBlueprint.create_from_node(
    _role_node["Tarot Reader"], recursively=True
)
