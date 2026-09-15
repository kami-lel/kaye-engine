"""
render_mode.py

define ``RenderMode``
"""

from enum import Flag, auto

__all__ = ("RenderMode",)


class RenderMode(Flag):
    """
    represent **render mode** as a *bit flag*, set on
    ``RenderProfile.mode`` to switch a blueprint's single prompt entry
    point between its otherwise-parallel rendering behaviors
    """

    # pylint: disable=invalid-name

    NORMAL = 0
    NEGATIVE = auto()
    IMAGE = auto()
