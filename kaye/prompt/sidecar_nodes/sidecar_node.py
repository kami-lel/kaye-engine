"""
sidecar_node.py

define ``SidecarNode``
"""

from kaye.prompt.prompt_corpus_node import PromptCorpusNode

__all__ = ("SidecarNode",)


class SidecarNode(PromptCorpusNode):
    """
    A sidecar node — a corpus node identified by ``{name}`` convention,
    attached to a blueprint but excluded from rendering by default.

    Sidecar nodes serve two roles:
    - **descriptor**: metadata fields (description, when_to_use, globs,
      prerequisite) always available on blueprint.sidecar
    - **conditional**: nodes like {for_claude} that are auto-checkmarked
      only when explicitly requested via contains_sidecar_nodes
    """

    pass
