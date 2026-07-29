from kaye_engine.prompt.blueprint import blueprint_registry
from kaye_engine.cli.exportable_abbr import EXPORTABLE_ABBRS


ALL_CLAUDE_SKILL_NAMES = [
    reg.skill_name
    for reg in blueprint_registry.values()
    if reg.skill_exportable
] + [
    g.skill_name
    for g in EXPORTABLE_ABBRS
]

TESTEE_CLAUDE_BEHAVIOR_CONTENT = [
    "## Claude Behavior",
    "Use `AGENTS.md` as the canonical instructions file",
    "Ignore `CLAUDE.md`",
    "When asked to update agent instructions, write to `AGENTS.md`",
]
