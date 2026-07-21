"""
registrations.py

the single place every blueprint is created; registers each one into
``BLUEPRINT_REGISTRIES`` via ``register_blueprint`` -- no blueprint should
be created anywhere else. other scripts must access blueprints through
``BLUEPRINT_REGISTRIES``, never by importing names from this module
"""

# pylint: disable=invalid-name

import functools

from .prompt_blueprint import PromptBlueprint
from .registry import register_blueprint

__all__ = ()


# FIXME poss mpv aux structure


# auxiliaries  #################################################################


_register_exportable = functools.partial(
    register_blueprint, skill_exportable=True, continue_exportable=True
)

_register_prompt = functools.partial(
    register_blueprint,
    skill_exportable=True,
    continue_exportable=True,
    llm_invokable=False,
)


# blueprints  ##################################################################
# (in corpus, but not as part of the content lines)


# Rapid
rapid = register_blueprint(
    "rapid",
    "Rapid",
    PromptBlueprint.parse("""    ○
[x] ├── Introduction
[x] └── Style Guide
[x]     └── Style Guide Markdown Format
[x]         └── Additional Markdown Format"""),
)
rapid.blueprint.sidecars.description = (
    "quick, mechanical text or data tasks with no persona or role"
)


# Chat
chat = register_blueprint(
    "chat",
    "Chat",
    PromptBlueprint.parse("""    ○
[x] ├── Introduction
[x] ├── Personality
[x] ├── Language
[x] ├── Style Guide
[x] │   ├── Style Guide Markdown Format
[x] │   │   └── Additional Markdown Format
[x] │   └── Style Guide Commentary Case
[x] └── (Abbreviations)"""),
)
chat.blueprint.sidecars.description = (
    "default for general conversation with full Kaye persona and role"
)


# Date and Time Format
date_time = _register_exportable(
    "date-time",
    "Date and Time Format",
    PromptBlueprint.create_from_node("Date and Time Format", recursively=True),
)

_corpus = date_time.blueprint.corpus


# Numerical Values with Units
number_unit = _register_exportable(
    "number-unit",
    "Numerical Values with Units",
    PromptBlueprint.create_from_node("Numerical Values with Units"),
)


# Triage Tags
triage_tags = _register_exportable(
    "triage-tags",
    "Triage Tags",
    PromptBlueprint.create_from_node(
        _corpus["Elements"]["Triage Tags"], recursively=True
    ),
)


# Coding Terms dynamic node
# (private combinator ingredient for `coder`; not independently exported)
coding_terms_blueprint = PromptBlueprint.parse(""" ○
[x] └── (Coding Terms)""")


# coder  =======================================================================

_kyc_node = _corpus["Kaye Peer Coder"]

# Coder
coder = _register_exportable(
    "coder",
    "Kaye Peer Coder",
    PromptBlueprint.create_from_node(_kyc_node)
    | triage_tags.blueprint
    | coding_terms_blueprint,
    always_apply=True,
)


# Coder Bash
coder_bash = _register_exportable(
    "coder-bash",
    "Coder Bash",
    PromptBlueprint.create_from_node(_kyc_node["Coder Bash"]),
)


# Coder C
coder_c = _register_exportable(
    "coder-c", "Coder C", PromptBlueprint.create_from_node(_kyc_node["Coder C"])
)
coder_c.blueprint.checkmark(_kyc_node["Brace Style"])


# Coder C++
coder_cpp = _register_exportable(
    "coder-cpp",
    "Coder CPP",
    PromptBlueprint.create_from_node(_kyc_node["Coder CPP"]),
)
coder_cpp.blueprint.checkmark(_kyc_node["Coder C"])
coder_cpp.blueprint.checkmark(_kyc_node["Brace Style"])


# Coder Unreal Engine
coder_ue = _register_exportable(
    "coder-ue",
    "Coder Unreal Engine",
    PromptBlueprint.create_from_node(_kyc_node["Coder Unreal Engine"]),
)
coder_ue.blueprint.checkmark(_kyc_node["Coder C"])
coder_ue.blueprint.checkmark(_kyc_node["Coder CPP"])
coder_ue.blueprint.checkmark(_kyc_node["Brace Style"])


# Coder C Sharp
coder_csharp = _register_exportable(
    "coder-csharp",
    "Coder C Sharp",
    PromptBlueprint.create_from_node(_kyc_node["Coder C Sharp"]),
)
coder_csharp.blueprint.checkmark(_kyc_node["Brace Style"])


# Coder Unity
coder_u3d = _register_exportable(
    "coder-u3d",
    "Coder Unity Engine",
    PromptBlueprint.create_from_node(
        _kyc_node["Coder Unity Engine"], recursively=True
    ),
)
coder_u3d.blueprint.checkmark(_kyc_node["Coder C Sharp"])
coder_u3d.blueprint.checkmark(_kyc_node["Brace Style"])


# Coder GDScript
coder_gdscript = _register_exportable(
    "coder-gdscript",
    "Coder GDScript",
    PromptBlueprint.create_from_node(_kyc_node["Coder GDScript"]),
)


# Coder HTML
coder_html = _register_exportable(
    "coder-html",
    "Coder HTML",
    PromptBlueprint.create_from_node(_kyc_node["Coder HTML"]),
)


# Coder JavaScript and TypeScript
coder_js_ts = _register_exportable(
    "coder-js-ts",
    "Coder JavaScript and TypeScript",
    PromptBlueprint.create_from_node(
        _kyc_node["Coder JavaScript and TypeScript"], recursively=True
    ),
)
coder_js_ts.blueprint.checkmark(_kyc_node["Brace Style"])


# Python  ----------------------------------------------------------------------
# Coder Python
coder_py = _register_exportable(
    "coder-py",
    "Coder Python",
    PromptBlueprint.create_from_node(_kyc_node["Coder Python"]),
)

# Coder Python Docstring
coder_py_docstring = _register_exportable(
    "coder-py-docstring",
    "Coder Python Docstring Style",
    PromptBlueprint.create_from_node(
        _kyc_node["Coder Python"]["Coder Python Docstring Style"]
    ),
)


# Coder Python Testing
coder_py_testing = _register_exportable(
    "coder-py-testing",
    "Coder Python Testing Guidelines",
    PromptBlueprint.create_from_node(
        _kyc_node["Coder Python"]["Coder Python Testing Guidelines"]
    ),
)


# Project  =====================================================================

_proj_node = _corpus["Projects"]

project_structure = _register_exportable(
    "project-structure",
    "Project Structure",
    PromptBlueprint.create_from_node(_proj_node["Project Structure"]),
)

# Project README Writer
project_readme = _register_exportable(
    "project-readme",
    "Project README Writer",
    PromptBlueprint.create_from_node(_proj_node["Project README Writer"]),
)

# Project CHANGELOG Writer
project_changelog = _register_exportable(
    "project-changelog",
    "Project CHANGELOG Writer",
    PromptBlueprint.create_from_node(
        _proj_node["Project CHANGELOG Writer"], recursively=True
    ),
)


# Project AGENTS Writer
project_agents = _register_exportable(
    "project-agents",
    "Project AGENTS Writer",
    PromptBlueprint.create_from_node(_proj_node["Project AGENTS Writer"]),
)

# Project Semantic Versioning
project_semantic_versioning = _register_exportable(
    "project-semantic-versioning",
    "Project Semantic Versioning",
    PromptBlueprint.create_from_node(_proj_node["Project Semantic Versioning"]),
)


# Style Guide  =================================================================

_style_node = _corpus["Style Guide"]


style = register_blueprint(
    "style",
    "Style Guide",
    PromptBlueprint.create_from_node(_style_node, recursively=True),
)


style_title_case = _register_exportable(
    "style-title-case",
    "Style Guide Title Case",
    PromptBlueprint.create_from_node(_style_node["Style Guide Title Case"]),
)

style_commentary_case = _register_exportable(
    "style-commentary-case",
    "Style Guide Commentary Case",
    PromptBlueprint.create_from_node(
        _style_node["Style Guide Commentary Case"]
    ),
)

style_briefness = _register_exportable(
    "style-briefness",
    "Style Guide Briefness Style",
    PromptBlueprint.create_from_node(
        _style_node["Style Guide Briefness Style"]
    ),
)

style_good_writing = _register_exportable(
    "style-good-writing",
    "Style Guide Good Writing",
    PromptBlueprint.create_from_node(_style_node["Style Guide Good Writing"]),
)


style_chicago_footnote = _register_exportable(
    "style-chicago-footnote",
    "Style Guide Chicago Footnote",
    PromptBlueprint.create_from_node(
        _style_node["Style Guide Chicago Footnote"]
    ),
)


# Prompt Engineering  ==========================================================

_prompt_engineer_node = _corpus["Prompt Engineering"]

prompt_writer = _register_exportable(
    "prompt-writer",
    "Prompt Writer",
    PromptBlueprint.create_from_node(
        _prompt_engineer_node["Prompt Writer"], recursively=True
    ),
)

description_writer = _register_exportable(
    "description-writer",
    "Skill Description Writer",
    PromptBlueprint.create_from_node(
        _prompt_engineer_node["Skill Description Writer"], recursively=True
    ),
)


# International Phonetic Alphabet  ============================================

ipa = _register_exportable(
    "ipa",
    "International Phonetic Alphabet",
    PromptBlueprint.create_from_node(
        _corpus["Elements"]["International Phonetic Alphabet"]
    ),
)


# Roles  =======================================================================

_role_node = _corpus["Role"]

role_art_tutor = _register_exportable(
    "role-art-tutor",
    "Art Tutor",
    PromptBlueprint.create_from_node(_role_node["Art Tutor"]),
)

role_assistant_barista = _register_exportable(
    "role-assistant-barista",
    "Assistant Barista",
    PromptBlueprint.create_from_node(
        _role_node["Assistant Barista"], recursively=True
    ),
)

role_deutschlehrer = _register_exportable(
    "role-deutschlehrer",
    "Deutschlehrer",
    PromptBlueprint.create_from_node(_role_node["Deutschlehrer"]),
)

role_editor = _register_exportable(
    "role-editor",
    "Editor",
    PromptBlueprint.create_from_node(_role_node["Editor"]),
)

role_librarian = _register_exportable(
    "role-librarian",
    "Librarian",
    PromptBlueprint.create_from_node(_role_node["Librarian"], recursively=True),
)

role_secretary = _register_exportable(
    "role-secretary",
    "Secretary",
    PromptBlueprint.create_from_node(_role_node["Secretary"]),
)

role_tarot_reader = _register_exportable(
    "role-tarot-reader",
    "Tarot Reader",
    PromptBlueprint.create_from_node(
        _role_node["Tarot Reader"], recursively=True
    ),
)


# Continue AI  ==================================================================
# (Continue-only, not exported as a Claude skill)

continue_behavior = register_blueprint(
    "continue-behavior",
    "Continue Behavior",
    PromptBlueprint.create_from_node(
        _corpus["Agent Behavior"]["Continue Behavior"]
    ),
    continue_exportable=True,
    always_apply=True,
)


# Prompts (invokable workflows)  ===============================================
# (share `_proj_node`, same "Projects" corpus node used above -- different
# children)

# Create README
create_readme = _register_prompt(
    "create-readme",
    "Create README",
    PromptBlueprint.create_from_node(
        _proj_node["Create README"], recursively=True
    ),
)

# Maintain README
maintain_readme = _register_prompt(
    "maintain-readme",
    "Maintain README",
    PromptBlueprint.create_from_node(_proj_node["Maintain README"]),
)

# Create CHANGELOG
create_changelog = _register_prompt(
    "create-changelog",
    "Create CHANGELOG",
    PromptBlueprint.create_from_node(_proj_node["Create CHANGELOG"]),
)

# Maintain CHANGELOG
maintain_changelog = _register_prompt(
    "maintain-changelog",
    "Maintain CHANGELOG",
    PromptBlueprint.create_from_node(
        _proj_node["Maintain CHANGELOG"], recursively=True
    ),
)

# Create AGENTS and CONTEXT
create_agents = _register_prompt(
    "create-agents",
    "Create AGENTS and CONTEXT",
    PromptBlueprint.create_from_node(
        _proj_node["Create AGENTS and CONTEXT"], recursively=True
    ),
)

# Maintain AGENTS and CONTEXT
maintain_agents = _register_prompt(
    "maintain-agents",
    "Maintain AGENTS and CONTEXT",
    PromptBlueprint.create_from_node(_proj_node["Maintain AGENTS and CONTEXT"]),
)

# Create Docs
create_docs = _register_prompt(
    "create-docs",
    "Create Docs",
    PromptBlueprint.create_from_node(_proj_node["Create Docs"]),
)

# Maintain Docs
maintain_docs = _register_prompt(
    "maintain-docs",
    "Maintain Docs",
    PromptBlueprint.create_from_node(
        _proj_node["Maintain Docs"], recursively=True
    ),
)

# Initialize Project
initialize_project = _register_prompt(
    "initialize-project",
    "Initialize Project",
    PromptBlueprint.create_from_node(_proj_node["Initialize Project"]),
)

# Prepare for Feature Landing
prepare_for_feature = _register_prompt(
    "prepare-for-feature",
    "Prepare for Feature Landing",
    PromptBlueprint.create_from_node(_proj_node["Prepare for Feature Landing"]),
)

# Prepare for Version Release
prepare_for_release = _register_prompt(
    "prepare-for-release",
    "Prepare for Version Release",
    PromptBlueprint.create_from_node(_proj_node["Prepare for Version Release"]),
)

# Plan for Step By Step
plan_step_by_step = _register_prompt(
    "plan-step-by-step",
    "Plan for Step By Step",
    PromptBlueprint.create_from_node(
        _proj_node["Plan for Step By Step"], recursively=True
    ),
)

# Resolve Merge Conflict
resolve_merge_conflict = _register_prompt(
    "resolve-merge-conflict",
    "Resolve Merge Conflict",
    PromptBlueprint.create_from_node(
        _proj_node["Resolve Merge Conflict"], recursively=True
    ),
)

# Gap Review
gap_review = _register_prompt(
    "gap-review",
    "Gap Review",
    PromptBlueprint.create_from_node(
        _proj_node["Gap Review"], recursively=True
    ),
)
