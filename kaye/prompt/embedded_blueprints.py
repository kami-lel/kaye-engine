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
)

# blueprints  ##################################################################

rapid_blueprint = PromptBlueprint.parse("""    ○
[x] ├── Introduction
[x] ├── Format
[x] └── {Abbreviations}""")


chat_blueprint = PromptBlueprint.parse("""    ○
[x] ├── Introduction
[x] ├── Personality
[x] ├── Language
[x] ├── Format
[x] ├── Role
[x] └── {Abbreviations}""")


date_time_blueprint = PromptBlueprint.parse("""    ○
[x] └── Elements
[x]     └── Date & Time Format""")


number_unit_blueprint = PromptBlueprint.parse("""    ○
[x] └── Elements
[x]     └── Numerical Values with Units""")


style_blueprint = PromptBlueprint.create_empty_blueprint()
style_blueprint.checkmark("Style", recursively=True)


annotation_marker_blueprint = PromptBlueprint.create_empty_blueprint()
annotation_marker_blueprint.checkmark(
    annotation_marker_blueprint.corpus["Elements"]["Annotation Markers"],
    recursively=True,
)


coder_bash_blueprint = PromptBlueprint.create_empty_blueprint()
coder_bash_blueprint.checkmark(
    coder_bash_blueprint.corpus["Kaye Peer Coder"]["Bash"]
)


coder_c_blueprint = PromptBlueprint.create_empty_blueprint()
_kyc_node = coder_c_blueprint.corpus["Kaye Peer Coder"]
coder_c_blueprint.checkmark(_kyc_node["C"])
coder_c_blueprint.checkmark(_kyc_node["Brace Style"])


coder_cpp_blueprint = PromptBlueprint.create_empty_blueprint()
_kyc_node = coder_cpp_blueprint.corpus["Kaye Peer Coder"]
coder_cpp_blueprint.checkmark(_kyc_node["C"])
coder_cpp_blueprint.checkmark(_kyc_node["C++"])
coder_cpp_blueprint.checkmark(_kyc_node["Brace Style"])


coder_ue_blueprint = PromptBlueprint.create_empty_blueprint()
_kyc_node = coder_ue_blueprint.corpus["Kaye Peer Coder"]
coder_ue_blueprint.checkmark(_kyc_node["C"])
coder_ue_blueprint.checkmark(_kyc_node["C++"])
coder_ue_blueprint.checkmark(_kyc_node["Unreal Engine"])
coder_ue_blueprint.checkmark(_kyc_node["Brace Style"])


coder_csharp_blueprint = PromptBlueprint.create_empty_blueprint()
_kyc_node = coder_csharp_blueprint.corpus["Kaye Peer Coder"]
coder_csharp_blueprint.checkmark(_kyc_node["C Sharp"])
coder_csharp_blueprint.checkmark(_kyc_node["Brace Style"])


coder_u3d_blueprint = PromptBlueprint.create_empty_blueprint()
_kyc_node = coder_u3d_blueprint.corpus["Kaye Peer Coder"]
coder_u3d_blueprint.checkmark(_kyc_node["C Sharp"])
coder_u3d_blueprint.checkmark(_kyc_node["Unity Engine"], recursively=True)
coder_u3d_blueprint.checkmark(_kyc_node["Brace Style"])


coder_gdscript_blueprint = PromptBlueprint.create_empty_blueprint()
coder_gdscript_blueprint.checkmark(
    coder_gdscript_blueprint.corpus["Kaye Peer Coder"]["GDScript"]
)


coder_html_blueprint = PromptBlueprint.create_empty_blueprint()
coder_html_blueprint.checkmark(
    coder_html_blueprint.corpus["Kaye Peer Coder"]["HTML"]
)


coder_js_ts_blueprint = PromptBlueprint.create_empty_blueprint()
_kyc_node = coder_js_ts_blueprint.corpus["Kaye Peer Coder"]
coder_js_ts_blueprint.checkmark(
    _kyc_node["JavaScript & TypeScript"], recursively=True
)
coder_js_ts_blueprint.checkmark(_kyc_node["Brace Style"])


coder_py_blueprint = PromptBlueprint.create_empty_blueprint()
coder_py_blueprint.checkmark(
    coder_py_blueprint.corpus["Kaye Peer Coder"]["Python"], recursively=True
)
