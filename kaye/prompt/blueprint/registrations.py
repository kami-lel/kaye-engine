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


def _register_node(
    register_fn, slug, container, name, *, recursively=False, **extra
):
    """
    register ``name`` looked up from ``container`` under ``slug`` via
    ``register_fn``, so ``name`` is written once instead of duplicated as
    both the display name and the node lookup key
    """
    return register_fn(
        slug,
        name,
        PromptBlueprint.create_from_node(
            container[name], recursively=recursively
        ),
        **extra,
    )


# blueprints  ##################################################################
# (in corpus, but not as part of the content lines)


# Rapid
rapid = register_blueprint(
    "rapid",
    "Rapid",
    PromptBlueprint.parse("""    ○
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
[x] ├── Personality
[x] │   └── Personality-Kaye
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
triage_tags = _register_node(
    _register_exportable,
    "triage-tags",
    _corpus["Elements"],
    "Triage Tags",
    recursively=True,
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

# Plan for Step By Step
plan_step_by_step = _register_node(
    _register_prompt,
    "plan-step-by-step",
    _kyc_node,
    "Plan for Step By Step",
    recursively=True,
)

# Sync Unit Test
sync_unit_test = _register_node(
    _register_prompt,
    "sync-unit-test",
    _kyc_node,
    "Sync Unit Test",
    recursively=True,
)

# Resolve Merge Conflict
resolve_merge_conflict = _register_node(
    _register_prompt,
    "resolve-merge-conflict",
    _kyc_node,
    "Resolve Merge Conflict",
    recursively=True,
)

# Gap Review
gap_review = _register_node(
    _register_prompt, "gap-review", _kyc_node, "Gap Review", recursively=True
)


# Coder Bash
coder_bash = _register_node(
    _register_exportable, "coder-bash", _kyc_node, "Coder Bash"
)


# Coder C
coder_c = _register_node(_register_exportable, "coder-c", _kyc_node, "Coder C")
coder_c.blueprint.checkmark(_kyc_node["Brace Style"])


# Coder C++
coder_cpp = _register_node(
    _register_exportable, "coder-cpp", _kyc_node, "Coder CPP"
)
coder_cpp.blueprint.checkmark(_kyc_node["Coder C"])
coder_cpp.blueprint.checkmark(_kyc_node["Brace Style"])


# Coder Unreal Engine
coder_ue = _register_node(
    _register_exportable, "coder-ue", _kyc_node, "Coder Unreal Engine"
)
coder_ue.blueprint.checkmark(_kyc_node["Coder C"])
coder_ue.blueprint.checkmark(_kyc_node["Coder CPP"])
coder_ue.blueprint.checkmark(_kyc_node["Brace Style"])


# Coder C Sharp
coder_csharp = _register_node(
    _register_exportable, "coder-csharp", _kyc_node, "Coder C Sharp"
)
coder_csharp.blueprint.checkmark(_kyc_node["Brace Style"])


# Coder Unity
coder_u3d = _register_node(
    _register_exportable,
    "coder-u3d",
    _kyc_node,
    "Coder Unity Engine",
    recursively=True,
)
coder_u3d.blueprint.checkmark(_kyc_node["Coder C Sharp"])
coder_u3d.blueprint.checkmark(_kyc_node["Brace Style"])


# Coder GDScript
coder_gdscript = _register_node(
    _register_exportable, "coder-gdscript", _kyc_node, "Coder GDScript"
)


# Coder HTML
coder_html = _register_node(
    _register_exportable, "coder-html", _kyc_node, "Coder HTML"
)


# Coder JavaScript and TypeScript
coder_js_ts = _register_node(
    _register_exportable,
    "coder-js-ts",
    _kyc_node,
    "Coder JavaScript and TypeScript",
    recursively=True,
)
coder_js_ts.blueprint.checkmark(_kyc_node["Brace Style"])


# Python  ----------------------------------------------------------------------
# Coder Python
coder_py = _register_node(
    _register_exportable, "coder-py", _kyc_node, "Coder Python"
)

# Coder Python Docstring
coder_py_docstring = _register_node(
    _register_exportable,
    "coder-py-docstring",
    _kyc_node["Coder Python"],
    "Coder Python Docstring Style",
)


# Coder Python Testing
coder_py_testing = _register_node(
    _register_exportable,
    "coder-py-testing",
    _kyc_node["Coder Python"],
    "Coder Python Testing Guidelines",
)


# Project  =====================================================================

_proj_node = _corpus["Projects"]

project_structure = _register_node(
    _register_exportable, "project-structure", _proj_node, "Project Structure"
)

# Project README Writer
project_readme = _register_node(
    _register_exportable, "project-readme", _proj_node, "Project README Writer"
)

# Project CHANGELOG Writer
project_changelog = _register_node(
    _register_exportable,
    "project-changelog",
    _proj_node,
    "Project CHANGELOG Writer",
    recursively=True,
)


# Project AGENTS Writer
project_agents = _register_node(
    _register_exportable, "project-agents", _proj_node, "Project AGENTS Writer"
)

# Project Semantic Versioning
project_semantic_versioning = _register_node(
    _register_exportable,
    "project-semantic-versioning",
    _proj_node,
    "Project Semantic Versioning",
)


# Style Guide  =================================================================

_style_node = _corpus["Style Guide"]


style = register_blueprint(
    "style",
    "Style Guide",
    PromptBlueprint.create_from_node(_style_node, recursively=True),
)


style_title_case = _register_node(
    _register_exportable,
    "style-title-case",
    _style_node,
    "Style Guide Title Case",
)

style_commentary_case = _register_node(
    _register_exportable,
    "style-commentary-case",
    _style_node,
    "Style Guide Commentary Case",
)

style_briefness = _register_node(
    _register_exportable,
    "style-briefness",
    _style_node,
    "Style Guide Briefness Style",
)

style_good_writing = _register_node(
    _register_exportable,
    "style-good-writing",
    _style_node,
    "Style Guide Good Writing",
)


style_chicago_footnote = _register_node(
    _register_exportable,
    "style-chicago-footnote",
    _style_node,
    "Style Guide Chicago Footnote",
)


# Prompt Engineering  ==========================================================

_prompt_engineer_node = _corpus["Prompt Engineering"]

prompt_writer = _register_node(
    _register_exportable,
    "prompt-writer",
    _prompt_engineer_node,
    "Prompt Writer",
    recursively=True,
)

description_writer = _register_node(
    _register_exportable,
    "description-writer",
    _prompt_engineer_node,
    "Skill Description Writer",
    recursively=True,
)


# International Phonetic Alphabet  ============================================

ipa = _register_node(
    _register_exportable,
    "ipa",
    _corpus["Elements"],
    "International Phonetic Alphabet",
)


# Roles  =======================================================================

_role_node = _corpus["Role"]

role_art_tutor = _register_node(
    _register_exportable, "role-art-tutor", _role_node, "Art Tutor"
)

role_assistant_barista = _register_node(
    _register_exportable,
    "role-assistant-barista",
    _role_node,
    "Assistant Barista",
    recursively=True,
)

role_deutschlehrer = _register_node(
    _register_exportable, "role-deutschlehrer", _role_node, "Deutschlehrer"
)

role_editor = _register_node(
    _register_exportable, "role-editor", _role_node, "Editor"
)

role_librarian = _register_node(
    _register_exportable,
    "role-librarian",
    _role_node,
    "Librarian",
    recursively=True,
)

role_secretary = _register_node(
    _register_exportable, "role-secretary", _role_node, "Secretary"
)

role_tarot_reader = _register_node(
    _register_exportable,
    "role-tarot-reader",
    _role_node,
    "Tarot Reader",
    recursively=True,
)


# Continue AI  ==================================================================
# (Continue-only, not exported as a Claude skill)

continue_behavior = _register_node(
    register_blueprint,
    "continue-behavior",
    _corpus["Agent Behavior"],
    "Continue Behavior",
    continue_exportable=True,
    always_apply=True,
)


# Prompts (invokable workflows)  ===============================================
# (share `_proj_node`, same "Projects" corpus node used above -- different
# children)

# Create README
create_readme = _register_node(
    _register_prompt,
    "create-readme",
    _proj_node,
    "Create README",
    recursively=True,
)

# Maintain README
maintain_readme = _register_node(
    _register_prompt, "maintain-readme", _proj_node, "Maintain README"
)

# Create CHANGELOG
create_changelog = _register_node(
    _register_prompt, "create-changelog", _proj_node, "Create CHANGELOG"
)

# Maintain CHANGELOG
maintain_changelog = _register_node(
    _register_prompt,
    "maintain-changelog",
    _proj_node,
    "Maintain CHANGELOG",
    recursively=True,
)

# Create AGENTS and CONTEXT
create_agents = _register_node(
    _register_prompt,
    "create-agents-and-context",
    _proj_node,
    "Create AGENTS and CONTEXT",
    recursively=True,
)

# Maintain AGENTS and CONTEXT
maintain_agents = _register_node(
    _register_prompt,
    "maintain-agents-and-context",
    _proj_node,
    "Maintain AGENTS and CONTEXT",
)

# Create Docs
create_docs = _register_node(
    _register_prompt, "create-docs", _proj_node, "Create Docs"
)

# Maintain Docs
maintain_docs = _register_node(
    _register_prompt,
    "maintain-docs",
    _proj_node,
    "Maintain Docs",
    recursively=True,
)

# Initialize Project
initialize_project = _register_node(
    _register_prompt, "initialize-project", _proj_node, "Initialize Project"
)

# Prepare for Feature Landing
prepare_for_feature = _register_node(
    _register_prompt,
    "prepare-for-feature",
    _proj_node,
    "Prepare for Feature Landing",
)

# Prepare for Version Release
prepare_for_release = _register_node(
    _register_prompt,
    "prepare-for-release",
    _proj_node,
    "Prepare for Version Release",
)

# Maintenance Before Compact
maintenance_before_compact = _register_node(
    _register_prompt,
    "maintenance-before-compact",
    _proj_node,
    "Maintenance Before Compact",
)
