"""
create_blueprint.py

common blueprints creations
"""

from kaye.prompt.prompt_blueprint import PromptBlueprint

__all__ = (
    "create_rapid_blueprint",
    "create_chat_blueprint",
    "create_coder_blueprint",
)


# pylint: disable=missing-function-docstring


# Blueprints  ##################################################################


RAPID_PROMPT_BLUEPRINT = """    ○
[x] ├── Introduction
[x] ├── Format
[x] └── {Abbreviations}"""


CHAT_PROMPT_BLUEPRINT = """    ○
[x] ├── Introduction
[x] ├── Personality
[x] ├── Language
[x] ├── Elements
[x] │   ├── Date & Time Format
[x] │   └── Numerical Values with Units
[x] ├── Format
[x] ├── Role
[x] └── {Abbreviations}"""


# creations  ###################################################################


def create_rapid_blueprint():
    return PromptBlueprint.parse(RAPID_PROMPT_BLUEPRINT)


def create_chat_blueprint():
    return PromptBlueprint.parse(CHAT_PROMPT_BLUEPRINT)


def create_coder_blueprint(plcs):  # TODO split various blueprints
    # create base bp from chat
    bp = create_chat_blueprint()

    # add styles
    bp.checkmark("Style", recursively=True)

    # add ams
    bp.checkmark(bp.corpus["Elements"]["Annotation Markers"], recursively=True)

    # add Kaye Peer Coder node
    kyc_node = bp.corpus["Kaye Peer Coder"]
    bp.checkmark(kyc_node)

    # adds PL nodes  -----------------------------------------------------------
    for plc in plcs.split(","):
        if plc == "bash":
            bp.checkmark(kyc_node["Bash"])

        elif plc == "c":
            bp.checkmark(kyc_node["C"])
            bp.checkmark(kyc_node["Brace Style"])

        elif plc == "cpp":
            bp.checkmark(kyc_node["C"])
            bp.checkmark(kyc_node["C++"])
            bp.checkmark(kyc_node["Brace Style"])

        elif plc == "ue":
            bp.checkmark(kyc_node["C"])
            bp.checkmark(kyc_node["C++"])
            bp.checkmark(kyc_node["Unreal Engine"])
            bp.checkmark(kyc_node["Brace Style"])

        elif plc == "csharp":
            bp.checkmark(kyc_node["C Sharp"])
            bp.checkmark(kyc_node["Brace Style"])

        elif plc == "u3d":
            bp.checkmark(kyc_node["C Sharp"])
            bp.checkmark(kyc_node["Unity Engine"], recursively=True)
            bp.checkmark(kyc_node["Brace Style"])

        elif plc == "gdscript":
            bp.checkmark(kyc_node["GDScript"])

        elif plc == "html":
            bp.checkmark(kyc_node["HTML"])

        elif plc in ("js", "ts"):
            bp.checkmark(kyc_node["JavaScript & TypeScript"], recursively=True)
            bp.checkmark(kyc_node["Brace Style"])

        elif plc == "py":
            bp.checkmark(kyc_node["Python"], recursively=True)

    return bp
