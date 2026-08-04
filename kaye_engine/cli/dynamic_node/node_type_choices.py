"""
node_type_choices.py

define ``NODE_TYPE_CHOICES``
"""

from kaye_engine.prompt.dynamic_nodes import (
    TodayNode,
    AbbrNode,
    UsableAbbrNode,
    LanguageCodeNode,
    PLCNode,
    UnityEngineAbbrNode,
    CodingTermsNode,
    PlanStepByStepAbbrNode,
    CodeDocumentationFieldAbbrNode,
)

__all__ = ("NODE_TYPE_CHOICES",)

# constants  ###################################################################
# map CLI-facing NODE_TYPE identifiers to their dynamic node class
NODE_TYPE_CHOICES = {
    "today": TodayNode,
    "abbr": AbbrNode,
    "usable": UsableAbbrNode,
    "language": LanguageCodeNode,
    "plc": PLCNode,
    "unity": UnityEngineAbbrNode,
    "coding": CodingTermsNode,
    "plan": PlanStepByStepAbbrNode,
    "docfield": CodeDocumentationFieldAbbrNode,
}
