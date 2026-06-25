from kaye.cli import EXPORTABLE_BLUEPRINTS
from kaye.cli.prompts_blueprints import PROMPTS_BLUEPRINTS
from kaye.cli.exportable_abbr import EXPORTABLE_ABBRS
from kaye.cli.claude import convert_display_name2skill_name


ALL_CLAUDE_SKILL_NAMES = [
    convert_display_name2skill_name(bp.display_name)
    for bp in EXPORTABLE_BLUEPRINTS + PROMPTS_BLUEPRINTS
] + [
    convert_display_name2skill_name(g.display_name)
    for g in EXPORTABLE_ABBRS
]

TESTEE_CLAUDE_BEHAVIOR_CONTENT = [
    "## Claude Behavior",
    "Use `AGENTS.md` as the canonical instructions file",
    "Ignore `CLAUDE.md`",
    "When asked to update agent instructions, write to `AGENTS.md`",
]
