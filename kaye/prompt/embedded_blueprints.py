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
    "coder_project_blueprint",
    "coder_readme_blueprint",
    "coder_changelog_blueprint",
    "coder_agents_blueprint",
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
)


# blueprints  ##################################################################
# TODO save description as part of prompt_corpus.md
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


# Numerical Values with Units
number_unit_blueprint = PromptBlueprint.create_from_node(
    "Numerical Values with Units"
)


# Style
style_blueprint = PromptBlueprint.create_empty_blueprint()
style_blueprint.checkmark("Style Guide", recursively=True)
style_blueprint.display_name = "Style Guide"
style_blueprint.description = (
    "writing tasks requiring house style and capitalization rules"
)


# Annotation Markers
annotation_marker_blueprint = PromptBlueprint.create_empty_blueprint()
annotation_marker_blueprint.checkmark(
    annotation_marker_blueprint.corpus["Elements"]["Annotation Markers"],
    recursively=True,
)
annotation_marker_blueprint.display_name = "Annotation Markers"
annotation_marker_blueprint.description = (
    "add-on when working with BUG, FIXME, TODO, or HACK markers in code or docs"
)


# coder  =======================================================================

_kyc_node = PromptBlueprint.create_empty_blueprint().corpus["Kaye Peer Coder"]

# Coder
coder_blueprint = PromptBlueprint.create_empty_blueprint()
coder_blueprint.checkmark("Kaye Peer Coder")
coder_blueprint.display_name = "Coder"
coder_blueprint.description = "instruction for coding and programming"


# Fixme change to "Repo Project Structure" "Repo README Writer" etc.
# Coder Project
coder_project_blueprint = PromptBlueprint.create_empty_blueprint()
coder_project_blueprint.checkmark(_kyc_node["Project Structure"])
coder_project_blueprint.display_name = "Project Structure"
coder_project_blueprint.description = (
    "generic Project/Repository structure for all programming languages"
)

# Coder Changelog
coder_changelog_blueprint = PromptBlueprint.create_empty_blueprint()
coder_changelog_blueprint.checkmark(
    _kyc_node["CHANGELOG Writer"], recursively=True
)
coder_changelog_blueprint.display_name = "Coder CHANGELOG Writer"
coder_changelog_blueprint.description = "format for CHANGELOG.md"


# Coder AGENTS Writer
coder_agents_blueprint = PromptBlueprint.create_empty_blueprint()
coder_agents_blueprint.checkmark(_kyc_node["AGENTS Writer"])
coder_agents_blueprint.display_name = "Coder AGENTS Writer"
coder_agents_blueprint.description = "format for AGENTS.md documentation"


# Coder README Writer
coder_readme_blueprint = PromptBlueprint.create_empty_blueprint()
coder_readme_blueprint.checkmark(_kyc_node["README Writer"])
coder_readme_blueprint.display_name = "Coder README Writer"
coder_readme_blueprint.description = "format for README documentation"


# Coder Bash
coder_bash_blueprint = PromptBlueprint.create_empty_blueprint()
coder_bash_blueprint.checkmark(_kyc_node["Bash"])
coder_bash_blueprint.display_name = "Coder Bash"
coder_bash_blueprint.description = (
    "Debian GNU/Linux shell commands; ready-to-run output"
)


# Coder C
coder_c_blueprint = PromptBlueprint.create_empty_blueprint()
coder_c_blueprint.checkmark(_kyc_node["C"])
coder_c_blueprint.checkmark(_kyc_node["Brace Style"])
coder_c_blueprint.display_name = "Coder C"
coder_c_blueprint.description = "C code (C99)"


# Coder C++
coder_cpp_blueprint = PromptBlueprint.create_empty_blueprint()
coder_cpp_blueprint.checkmark(_kyc_node["C"])
coder_cpp_blueprint.checkmark(_kyc_node["C++"])
coder_cpp_blueprint.checkmark(_kyc_node["Brace Style"])
coder_cpp_blueprint.display_name = "Coder CPP"
coder_cpp_blueprint.description = "C++ code (C++17)"


# Coder Unreal Engine
coder_ue_blueprint = PromptBlueprint.create_empty_blueprint()
coder_ue_blueprint.checkmark(_kyc_node["C"])
coder_ue_blueprint.checkmark(_kyc_node["C++"])
coder_ue_blueprint.checkmark(_kyc_node["Unreal Engine"])
coder_ue_blueprint.checkmark(_kyc_node["Brace Style"])
coder_ue_blueprint.display_name = "Coder Unreal Engine"
coder_ue_blueprint.description = "C++ code for Unreal Engine"


# Coder C Sharp
coder_csharp_blueprint = PromptBlueprint.create_empty_blueprint()
coder_csharp_blueprint.checkmark(_kyc_node["C Sharp"])
coder_csharp_blueprint.checkmark(_kyc_node["Brace Style"])
coder_csharp_blueprint.display_name = "Coder C Sharp"
coder_csharp_blueprint.description = "C# code"


# Coder Unity
coder_u3d_blueprint = PromptBlueprint.create_empty_blueprint()
coder_u3d_blueprint.checkmark(_kyc_node["C Sharp"])
coder_u3d_blueprint.checkmark(_kyc_node["Unity Engine"], recursively=True)
coder_u3d_blueprint.checkmark(_kyc_node["Brace Style"])
coder_u3d_blueprint.display_name = "Coder Unity"
coder_u3d_blueprint.description = (
    "C# code for Unity 6 (MonoBehaviour scripts, components, Inspector fields)"
)


# Coder GDScript
coder_gdscript_blueprint = PromptBlueprint.create_empty_blueprint()
coder_gdscript_blueprint.checkmark(_kyc_node["GDScript"])
coder_gdscript_blueprint.display_name = "Coder GDScript"
coder_gdscript_blueprint.description = "GDScript code for Godot 4"


# Coder HTML
coder_html_blueprint = PromptBlueprint.create_empty_blueprint()
coder_html_blueprint.checkmark(_kyc_node["HTML"])
coder_html_blueprint.display_name = "Coder HTML"
coder_html_blueprint.description = "HTML5 markup"


# Coder JavaScript and TypeScript
coder_js_ts_blueprint = PromptBlueprint.create_empty_blueprint()
coder_js_ts_blueprint.checkmark(
    _kyc_node["JavaScript & TypeScript"], recursively=True
)
coder_js_ts_blueprint.checkmark(_kyc_node["Brace Style"])
coder_js_ts_blueprint.display_name = "Coder JavaScript and TypeScript"
coder_js_ts_blueprint.description = "JavaScript or TypeScript code"


# Python  ----------------------------------------------------------------------
# Coder Python
coder_py_blueprint = PromptBlueprint.create_empty_blueprint()
coder_py_blueprint.checkmark(_kyc_node["Python"])
coder_py_blueprint.display_name = "Coder Python"
coder_py_blueprint.description = "Python code"


# Coder Python Docstring
coder_py_docstring_blueprint = PromptBlueprint.create_empty_blueprint()
coder_py_docstring_blueprint.checkmark(_kyc_node["Python"]["Docstring Style"])
coder_py_docstring_blueprint.display_name = "Coder Python Docstring"
coder_py_docstring_blueprint.description = (
    "Python docstrings in Sphinx/reStructuredText style"
)


# Coder Python Testing
coder_py_testing_blueprint = PromptBlueprint.create_empty_blueprint()
coder_py_testing_blueprint.checkmark(_kyc_node["Python"]["Testing Guidelines"])
coder_py_testing_blueprint.display_name = "Coder Python Testing"
coder_py_testing_blueprint.description = (
    "Python tests using pytest with Test classes and test_ functions"
)
