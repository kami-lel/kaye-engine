"""
affordance_registry.py

define ``Affordance``, ``Variant``, ``affordance_registry``,
``variant_registry``, ``register_variant`` -- the two-level registry a
consumer project populates with the platform capabilities its corpus
can conditionally acknowledge

an ``Affordance`` is a conceptual capability family (e.g.
"ask-user-question"); a ``Variant`` is one concrete implementation of
that family (e.g. ``ask_user_input_v0``), linked to it via
``affordance_name``. A corpus authors a ``{[variant canonical_name]
Usage}`` sidecar per variant, and a ``{[affordance canonical_name]
Fallback}`` sidecar per family, checkmarked when every variant
registered under that family is unavailable
"""

from dataclasses import dataclass

__all__ = (
    "Affordance",
    "Variant",
    "affordance_registry",
    "register_variant",
    "variant_registry",
)


@dataclass(kw_only=True)
class Affordance:
    """
    a registered capability family, and the sidecar name derived from
    its ``canonical_name`` a corpus may author to describe the case
    where every variant of it is unavailable


    :param canonical_name: unique identifier for this affordance
    :type canonical_name: str
    """

    canonical_name: str

    @property
    def fallback_sidecar_name(self):
        """
        :return: the sidecar name a corpus author checkmarks content
                under to describe the absence of every variant of this
                affordance
        :rtype: str
        """
        return "[{}] Fallback".format(self.canonical_name)


@dataclass(kw_only=True)
class Variant:
    """
    a single registered concrete implementation of an ``Affordance``,
    and the sidecar name derived from its ``canonical_name`` a corpus
    may author to describe using it


    :param canonical_name: unique identifier for this variant
    :type canonical_name: str
    :param affordance_name: canonical name of the ``Affordance`` this
            variant implements
    :type affordance_name: str
    """

    canonical_name: str
    affordance_name: str

    @property
    def usage_sidecar_name(self):
        """
        :return: the sidecar name a corpus author checkmarks content
                under to describe using this variant
        :rtype: str
        """
        return "[{}] Usage".format(self.canonical_name)


affordance_registry = {}
variant_registry = {}


# auxiliaries  #################################################################
def _register_affordance(canonical_name):
    """
    register a new `Affordance` under `canonical_name`, for
    `register_variant` to call when auto-creating one
    """
    if canonical_name in affordance_registry:
        raise ValueError(
            "duplicate affordance registry name: {}".format(canonical_name)
        )

    affordance = Affordance(canonical_name=canonical_name)
    affordance_registry[canonical_name] = affordance

    return affordance


# Main Entry Point  ############################################################
def register_variant(canonical_name, affordance_name):
    """
    construct a `Variant` and insert it into `variant_registry` under
    its `canonical_name`, linked to the `Affordance` named
    `affordance_name` -- registering that affordance first when it
    isn't already registered

    the single entry point for registering a variant, whether it is
    the first (and possibly only) variant of a fresh affordance, or an
    additional variant of one already registered


    :param canonical_name: unique identifier for the variant
    :type canonical_name: str
    :param affordance_name: affordance this variant implements
    :type affordance_name: str
    :raises ValueError: `canonical_name` already registered
    :return: the newly registered variant
    :rtype: Variant
    :example:
    >>> register_variant("ask_user_input_v0", "ask-user-question")
    >>> register_variant("AskUserQuestion", "ask-user-question")
    """
    if canonical_name in variant_registry:
        raise ValueError(
            "duplicate variant registry name: {}".format(canonical_name)
        )

    if affordance_name not in affordance_registry:
        _register_affordance(affordance_name)

    variant = Variant(
        canonical_name=canonical_name, affordance_name=affordance_name
    )
    variant_registry[canonical_name] = variant

    return variant
