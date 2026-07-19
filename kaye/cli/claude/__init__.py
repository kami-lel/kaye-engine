"""
CLI subcommand for Anthropic Claude Skill & Plugin integration.
"""

from kaye.prompt.sidecar_nodes import SidecarNodeType

# sidecar node types to auto-checkmark when exporting Claude prompts
CONTAINING_SIDECAR_NODES = (
    SidecarNodeType.FOR_CLAUDE | SidecarNodeType.PREREQUISITE
)
