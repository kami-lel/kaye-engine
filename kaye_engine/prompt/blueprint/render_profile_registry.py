"""
render_profile_registry.py

define ``RenderProfileEntry``, ``render_profile_registry`` and
``register_render_profile`` -- the named render profiles ``--surface``
chooses from
"""

from dataclasses import dataclass

from .render_profile import RenderProfile

__all__ = (
    "RenderProfileEntry",
    "register_render_profile",
    "render_profile_registry",
)


@dataclass(frozen=True, kw_only=True)
class RenderProfileEntry:
    """
    one registered render profile, with its human-readable remark


    :param name: unique registry key, also the ``--surface`` name
    :type name: str
    :param profile: the registered render settings
    :type profile: RenderProfile
    :param remark: simple description of what the profile targets;
            empty when none was given
    :type remark: str
    """

    name: str
    profile: RenderProfile
    remark: str = ""


# name -> entry, in registration order
render_profile_registry = {}


# Main Entry Point  ############################################################
def register_render_profile(name, profile, remark=""):
    """
    insert a ``RenderProfileEntry`` into ``render_profile_registry``
    under ``name``


    :param name: unique registry key, also the ``--surface`` name
    :type name: str
    :param profile: the render settings to register
    :type profile: RenderProfile
    :param remark: simple description of what the profile targets;
            defaults to ``""``
    :type remark: str, optional
    :raises ValueError: ``name`` already registered
    :raises TypeError: ``remark`` is not a ``str``
    :return: the newly registered entry
    :rtype: RenderProfileEntry
    :example:
    >>> register_render_profile("plain", RenderProfile(), "no extras")
    """
    if not isinstance(remark, str):
        raise TypeError(
            "render profile remark must be str, got {}".format(
                type(remark).__name__
            )
        )

    if name in render_profile_registry:
        raise ValueError(
            "duplicate render profile registry name: {}".format(name)
        )

    entry = RenderProfileEntry(name=name, profile=profile, remark=remark)
    render_profile_registry[name] = entry

    return entry
