"""
affordance_registry.py

define ``Affordance``, ``affordance_registry``, ``register_affordance``,
``get_affordance`` -- the registry a consumer project populates with the
platform capabilities its corpus can conditionally acknowledge via a
paired ``{name Usage}`` / ``{name Lack}`` sidecar
"""

from dataclasses import dataclass

__all__ = (
    "Affordance",
    "affordance_registry",
    "register_affordance",
    "get_affordance",
)


@dataclass(kw_only=True)
class Affordance:
    """
    a single registered platform capability, and the two sidecar names
    derived from its ``canonical_name`` that a corpus may author


    :param canonical_name: unique identifier for this affordance; also
            the shared root of its ``Usage``/``Lack`` sidecar names, and
            the string a consumer's ``affordances=(...)`` tuple names to
            mark it available
    :type canonical_name: str
    :param display_name: human-readable name, used in generated
            documentation
    :type display_name: str
    :param remark: one-line description of what this affordance does
    :type remark: str, optional
    """

    canonical_name: str
    display_name: str
    remark: str = ""

    @property
    def usage_sidecar_name(self):
        """
        :return: the sidecar name a corpus author checkmarks content
                under to describe using this affordance
        :rtype: str
        """
        return "{} Usage".format(self.canonical_name)

    @property
    def lack_sidecar_name(self):
        """
        :return: the sidecar name a corpus author checkmarks content
                under to describe the absence of this affordance
        :rtype: str
        """
        return "{} Lack".format(self.canonical_name)


# Entry Point  #################################################################

affordance_registry = {}


def register_affordance(canonical_name, display_name, remark=""):
    """
    construct an `Affordance` and insert it into `affordance_registry`
    under its `canonical_name`


    :param canonical_name: unique identifier for the affordance
    :type canonical_name: str
    :param display_name: human-readable name
    :type display_name: str
    :param remark: one-line description of what the affordance does
    :type remark: str, optional
    :raises ValueError: `canonical_name` is already registered
    :return: the newly registered affordance
    :rtype: Affordance
    :example:
    >>> register_affordance(
    ...     "Claude Tool:TodoWrite", "TodoWrite",
    ...     remark="maintains a task/todo list for the session",
    ... )
    """
    if canonical_name in affordance_registry:
        raise ValueError(
            "duplicate affordance registry name: {}".format(canonical_name)
        )

    affordance = Affordance(
        canonical_name=canonical_name,
        display_name=display_name,
        remark=remark,
    )
    affordance_registry[canonical_name] = affordance

    return affordance


def get_affordance(canonical_name):
    """
    :param canonical_name: canonical name an affordance was registered
            under via `register_affordance`
    :type canonical_name: str
    :raises KeyError: no affordance is registered under ``canonical_name``
    :return: the registry entry stored under ``canonical_name``
    :rtype: Affordance
    :example:
    >>> get_affordance("Claude Tool:TodoWrite")
    """
    try:
        return affordance_registry[canonical_name]
    except KeyError as e:
        raise KeyError(
            "no affordance registered under name: {}".format(canonical_name)
        ) from e
