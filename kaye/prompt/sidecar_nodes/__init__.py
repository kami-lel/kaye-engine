"""
sidecar_nodes

nodes attached to a blueprint's parent node but stored as corpus content,
identified by the ``{name}`` heading convention; excluded by default and
conditionally spliced in via ``contains_sidecar_nodes`` when their parent is
checkmarked
"""

from .sidecar_node_type import SidecarNodeType
from .blueprint_description_sidecars import BlueprintDescriptorSidecars

__all__ = (
    "SidecarNodeType",
    "BlueprintDescriptorSidecars",
)
