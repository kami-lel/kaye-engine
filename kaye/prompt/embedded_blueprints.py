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
    "annotation_marker_blueprint",
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
    "style_capitalization_blueprint",
    "style_briefness_blueprint",
    "style_good_writing_blueprint",
)


# blueprints  ##################################################################
# (in corpus, but not as part of the content lines)

# Rapid
rapid_blueprint = PromptBlueprint.parse("""    ○
[x] ├── Introduction
[x] ├── Format
[x] └── {Abbreviations}""")
rapid_blueprint.display_name = "Rapid"
rapid_blueprint.description = (
    "quick, mechanical text or data tasks with no persona or role"
)


# Chat
chat_blueprint = PromptBlueprint.parse("""    ○
[x] ├── Introduction
[x] ├── Personality
[x] ├── Language
[x] ├── Format
[x] ├── Role
[x] └── {Abbreviations}""")
chat_blueprint.display_name = "Chat"
chat_blueprint.description = (
    "default for general conversation with full Kaye persona and role"
)


# Date and Time Format
date_time_blueprint = PromptBlueprint.create_from_node("Date and Time Format")

_corpus = date_time_blueprint.corpus


# Numerical Values with Units
number_unit_blueprint = PromptBlueprint.create_from_node(
    "Numerical Values with Units"
)


# Annotation Markers
annotation_marker_blueprint = PromptBlueprint.create_from_node(
    _corpus["Elements"]["Annotation Markers"],
    recursively=True,
)


# coder  =======================================================================

_kyc_node = _corpus["Kaye Peer Coder"]

# Coder
coder_blueprint = PromptBlueprint.create_from_node(_kyc_node)


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


style_capitalization_blueprint = PromptBlueprint.create_from_node(
    _style_node["Style Guide Capitalization"], recursively=True
)

style_briefness_blueprint = PromptBlueprint.create_from_node(
    _style_node["Style Guide Briefness Style"]
)

style_good_writing_blueprint = PromptBlueprint.create_from_node(
    _style_node["Style Guide Good Writing"]
)
