"""
embedded_blueprints.py

common blueprints creations
"""

from kaye.prompt.prompt_blueprint import PromptBlueprint

__all__ = (
    "rapid_blueprint",
    "chat_blueprint",
    "date_time_blueprint",
    "number_unit_blueprint",
    "style_blueprint",
    "annotation_marker_blueprint",
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
    "coder_py_test_blueprint",
)

# blueprints  ##################################################################

rapid_blueprint = PromptBlueprint.parse("""    ○
[x] ├── Introduction
[x] ├── Format
[x] └── {Abbreviations}""")
rapid_blueprint.display_name = "Rapid"
rapid_blueprint.description = (
    "quick, mechanical text or data tasks with no persona or role"
)


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


date_time_blueprint = PromptBlueprint.parse("""    ○
[x] └── Elements
[x]     └── Date & Time Format""")
date_time_blueprint.display_name = "Date and Time Format"
date_time_blueprint.description = "add-on when dates or times appear in output"


number_unit_blueprint = PromptBlueprint.parse("""    ○
[x] └── Elements
[x]     └── Numerical Values with Units""")
number_unit_blueprint.display_name = "Numerical Values with Units"
number_unit_blueprint.description = (
    "add-on when physical quantities appear in output"
)


style_blueprint = PromptBlueprint.create_empty_blueprint()
style_blueprint.checkmark("Style", recursively=True)
style_blueprint.display_name = "Style"
style_blueprint.description = (
    "add-on for writing tasks requiring house style and capitalization rules"
)


annotation_marker_blueprint = PromptBlueprint.create_empty_blueprint()
annotation_marker_blueprint.checkmark(
    annotation_marker_blueprint.corpus["Elements"]["Annotation Markers"],
    recursively=True,
)
annotation_marker_blueprint.display_name = "Annotation Markers"
annotation_marker_blueprint.description = (
    "add-on when working with BUG, FIXME, TODO, or HACK markers in code or docs"
)


coder_bash_blueprint = PromptBlueprint.create_empty_blueprint()
coder_bash_blueprint.checkmark(
    coder_bash_blueprint.corpus["Kaye Peer Coder"]["Bash"]
)
coder_bash_blueprint.display_name = "Coder Bash"
coder_bash_blueprint.description = (
    "Debian GNU/Linux shell commands; ready-to-run output, no explanation"
)


coder_c_blueprint = PromptBlueprint.create_empty_blueprint()
_kyc_node = coder_c_blueprint.corpus["Kaye Peer Coder"]
coder_c_blueprint.checkmark(_kyc_node["C"])
coder_c_blueprint.checkmark(_kyc_node["Brace Style"])
coder_c_blueprint.display_name = "Coder C"
coder_c_blueprint.description = "C code (C99)"


coder_cpp_blueprint = PromptBlueprint.create_empty_blueprint()
_kyc_node = coder_cpp_blueprint.corpus["Kaye Peer Coder"]
coder_cpp_blueprint.checkmark(_kyc_node["C"])
coder_cpp_blueprint.checkmark(_kyc_node["C++"])
coder_cpp_blueprint.checkmark(_kyc_node["Brace Style"])
coder_cpp_blueprint.display_name = "Coder CPP"
coder_cpp_blueprint.description = "C++ code (C++17)"


coder_ue_blueprint = PromptBlueprint.create_empty_blueprint()
_kyc_node = coder_ue_blueprint.corpus["Kaye Peer Coder"]
coder_ue_blueprint.checkmark(_kyc_node["C"])
coder_ue_blueprint.checkmark(_kyc_node["C++"])
coder_ue_blueprint.checkmark(_kyc_node["Unreal Engine"])
coder_ue_blueprint.checkmark(_kyc_node["Brace Style"])
coder_ue_blueprint.display_name = "Coder Unreal Engine"
coder_ue_blueprint.description = "C++ code for Unreal Engine"


coder_csharp_blueprint = PromptBlueprint.create_empty_blueprint()
_kyc_node = coder_csharp_blueprint.corpus["Kaye Peer Coder"]
coder_csharp_blueprint.checkmark(_kyc_node["C Sharp"])
coder_csharp_blueprint.checkmark(_kyc_node["Brace Style"])
coder_csharp_blueprint.display_name = "Coder C Sharp"
coder_csharp_blueprint.description = "C# code"


coder_u3d_blueprint = PromptBlueprint.create_empty_blueprint()
_kyc_node = coder_u3d_blueprint.corpus["Kaye Peer Coder"]
coder_u3d_blueprint.checkmark(_kyc_node["C Sharp"])
coder_u3d_blueprint.checkmark(_kyc_node["Unity Engine"], recursively=True)
coder_u3d_blueprint.checkmark(_kyc_node["Brace Style"])
coder_u3d_blueprint.display_name = "Coder Unity"
coder_u3d_blueprint.description = (
    "C# code for Unity 6 (MonoBehaviour scripts, components, Inspector fields)"
)


coder_gdscript_blueprint = PromptBlueprint.create_empty_blueprint()
coder_gdscript_blueprint.checkmark(
    coder_gdscript_blueprint.corpus["Kaye Peer Coder"]["GDScript"]
)
coder_gdscript_blueprint.display_name = "Coder GDScript"
coder_gdscript_blueprint.description = "GDScript code for Godot 4"


coder_html_blueprint = PromptBlueprint.create_empty_blueprint()
coder_html_blueprint.checkmark(
    coder_html_blueprint.corpus["Kaye Peer Coder"]["HTML"]
)
coder_html_blueprint.display_name = "Coder HTML"
coder_html_blueprint.description = "HTML5 markup"


coder_js_ts_blueprint = PromptBlueprint.create_empty_blueprint()
_kyc_node = coder_js_ts_blueprint.corpus["Kaye Peer Coder"]
coder_js_ts_blueprint.checkmark(
    _kyc_node["JavaScript & TypeScript"], recursively=True
)
coder_js_ts_blueprint.checkmark(_kyc_node["Brace Style"])
coder_js_ts_blueprint.display_name = "Coder JavaScript and TypeScript"
coder_js_ts_blueprint.description = "JavaScript or TypeScript code"


coder_py_blueprint = PromptBlueprint.create_empty_blueprint()
coder_py_blueprint.checkmark(
    coder_py_blueprint.corpus["Kaye Peer Coder"]["Python"]
)
coder_py_blueprint.display_name = "Coder Python"
coder_py_blueprint.description = "Python code"

coder_py_docstring_blueprint = PromptBlueprint.create_empty_blueprint()
coder_py_docstring_blueprint.checkmark(
    coder_py_docstring_blueprint.corpus["Kaye Peer Coder"]["Python"][
        "Docstring Style"
    ]
)
coder_py_docstring_blueprint.display_name = "Coder Python Docstring"

coder_py_docstring_blueprint.description = (
    "Python docstrings in Sphinx/reStructuredText style"
)

coder_py_test_blueprint = PromptBlueprint.create_empty_blueprint()
coder_py_test_blueprint.checkmark(
    coder_py_test_blueprint.corpus["Kaye Peer Coder"]["Python"][
        "Testing Guidelines"
    ]
)
coder_py_test_blueprint.display_name = "Coder Python Testing"
coder_py_test_blueprint.description = (
    "Python tests using pytest with Test classes and test_ functions"
)
