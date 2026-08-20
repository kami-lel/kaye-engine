"""
affordance_registry.py

define ``Affordance``, ``affordance_registry``, ``register_affordance``
-- the registry a consumer project populates with the platform
capabilities its corpus can conditionally acknowledge via a paired
``{name Usage}`` / ``{name Lack}`` sidecar
"""

from dataclasses import dataclass

__all__ = (
    "Affordance",
    "affordance_registry",
    "register_affordance",
)


@dataclass(kw_only=True)
class Affordance:
    """
    a single registered platform capability, and the two sidecar names
    derived from its ``canonical_name`` that a corpus may author


    :param canonical_name: unique identifier for this affordance
    :type canonical_name: str
    """

    canonical_name: str

    @property
    def usage_sidecar_name(self):
        """
        :return: the sidecar name a corpus author checkmarks content
                under to describe using this affordance
        :rtype: str
        """
        return "[{}] Usage".format(self.canonical_name)

    @property
    def lack_sidecar_name(self):
        """
        :return: the sidecar name a corpus author checkmarks content
                under to describe the absence of this affordance
        :rtype: str
        """
        return "[{}] Lack".format(self.canonical_name)


affordance_registry = {}


# Main Entry Point  ############################################################
def register_affordance(canonical_name):
    """
    construct an `Affordance` and insert it into `affordance_registry`
    under its `canonical_name`


    :param canonical_name: unique identifier for the affordance
    :type canonical_name: str
    :raises ValueError: `canonical_name` is already registered
    :return: the newly registered affordance
    :rtype: Affordance
    :example:
    >>> register_affordance("ClaudeCode:TodoWrite")
    """
    if canonical_name in affordance_registry:
        raise ValueError(
            "duplicate affordance registry name: {}".format(canonical_name)
        )

    affordance = Affordance(canonical_name=canonical_name)
    affordance_registry[canonical_name] = affordance

    return affordance
