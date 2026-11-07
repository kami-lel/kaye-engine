"""
affordance_registry.py

define ``Affordance``, ``Variant``, ``affordance_registry``,
``variant_registry``, ``register_affordance``, ``register_variant`` --
the two-level registry a consumer project populates with the platform
capabilities its corpus can conditionally acknowledge

an ``Affordance`` is a conceptual capability family (e.g.
"ask-user-question"); a ``Variant`` is one concrete implementation of
that family (e.g. ``ask_user_input_v0``), linked to it via
``affordance_name``. Each carries an optional ``remark``, a simple
description that is its de facto documentation. A corpus authors ``{[variant canonical_name]
Usage}``/``Lack`` sidecars per variant, checkmarked when that variant
is present/absent, and ``{[affordance canonical_name] Usage}``/
``Fallback`` sidecars per family, checkmarked when any/none of its
variants are present
"""

from dataclasses import dataclass

__all__ = (
    "Affordance",
    "Variant",
    "affordance_registry",
    "register_affordance",
    "register_variant",
    "variant_registry",
)


@dataclass(kw_only=True)
class Affordance:
    """
    a registered capability family, and the ``Usage``/``Fallback``
    sidecar names derived from its ``canonical_name``


    :param canonical_name: unique identifier for this affordance
    :type canonical_name: str
    :param remark: simple description of the capability; empty when
            none was given
    :type remark: str
    """

    canonical_name: str
    remark: str = ""

    @property
    def usage_sidecar_name(self):
        """
        :return: the sidecar name checkmarked when any variant of
                this affordance is present
        :rtype: str
        """
        return "[{}] Usage".format(self.canonical_name)

    @property
    def fallback_sidecar_name(self):
        """
        :return: the sidecar name checkmarked when every variant of
                this affordance is absent
        :rtype: str
        """
        return "[{}] Fallback".format(self.canonical_name)


@dataclass(kw_only=True)
class Variant:
    """
    a single registered concrete implementation of an ``Affordance``,
    and the ``Usage``/``Lack`` sidecar names derived from its
    ``canonical_name``


    :param canonical_name: unique identifier for this variant
    :type canonical_name: str
    :param affordance_name: canonical name of the ``Affordance`` this
            variant implements
    :type affordance_name: str
    :param remark: simple description of the implementation; empty
            when none was given
    :type remark: str
    """

    canonical_name: str
    affordance_name: str
    remark: str = ""

    @property
    def usage_sidecar_name(self):
        """
        :return: the sidecar name checkmarked when this variant is
                present
        :rtype: str
        """
        return "[{}] Usage".format(self.canonical_name)

    @property
    def lack_sidecar_name(self):
        """
        :return: the sidecar name checkmarked when this variant is
                absent
        :rtype: str
        """
        return "[{}] Lack".format(self.canonical_name)


affordance_registry = {}
variant_registry = {}


# auxiliaries  #################################################################
def _check_remark(remark, kind):
    """
    raise `TypeError` unless `remark` is a `str`; `kind` names the
    registry in the message
    """
    if not isinstance(remark, str):
        raise TypeError(
            "{} remark must be str, got {}".format(kind, type(remark).__name__)
        )


# Main Entry Points  ###########################################################
def register_affordance(canonical_name, remark=""):
    """
    construct an `Affordance` and insert it into `affordance_registry`
    under its `canonical_name`

    register an affordance before any variant names it as its
    `affordance_name`


    :param canonical_name: unique identifier for the affordance
    :type canonical_name: str
    :param remark: simple description of the capability; defaults to
            ``""``
    :type remark: str, optional
    :raises ValueError: `canonical_name` already registered
    :raises TypeError: `remark` is not a `str`
    :return: the newly registered affordance
    :rtype: Affordance
    :example:
    >>> register_affordance("ask-user-question", "ask questions")
    """
    _check_remark(remark, "affordance")

    if canonical_name in affordance_registry:
        raise ValueError(
            "duplicate affordance registry name: {}".format(canonical_name)
        )

    affordance = Affordance(canonical_name=canonical_name, remark=remark)
    affordance_registry[canonical_name] = affordance

    return affordance


def register_variant(canonical_name, affordance_name, remark=""):
    """
    construct a `Variant` and insert it into `variant_registry` under
    its `canonical_name`, linked to the `Affordance` named
    `affordance_name`, which must already be registered


    :param canonical_name: unique identifier for the variant
    :type canonical_name: str
    :param affordance_name: affordance this variant implements
    :type affordance_name: str
    :param remark: simple description of the implementation; defaults
            to ``""``
    :type remark: str, optional
    :raises ValueError: `canonical_name` already registered
    :raises KeyError: `affordance_name` not registered
    :raises TypeError: `remark` is not a `str`
    :return: the newly registered variant
    :rtype: Variant
    :example:
    >>> register_affordance("ask-user-question")
    >>> register_variant("ask_user_input_v0", "ask-user-question")
    >>> register_variant("AskUserQuestion", "ask-user-question")
    """
    _check_remark(remark, "variant")

    if canonical_name in variant_registry:
        raise ValueError(
            "duplicate variant registry name: {}".format(canonical_name)
        )

    if affordance_name not in affordance_registry:
        raise KeyError(
            "unregistered affordance name: {}".format(affordance_name)
        )

    variant = Variant(
        canonical_name=canonical_name,
        affordance_name=affordance_name,
        remark=remark,
    )
    variant_registry[canonical_name] = variant

    return variant
