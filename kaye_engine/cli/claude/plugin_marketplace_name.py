"""
plugin_marketplace_name.py

define ``set_claude_plugin_marketplace_name``
"""

from kaye_engine.cli import claude

__all__ = ("set_claude_plugin_marketplace_name",)


# Public API  ###################################################################
def set_claude_plugin_marketplace_name(name):
    """
    set the name shown to Anthropic's plugin/marketplace tooling

    :param name: plugin/marketplace name, used in manifest and folder
            name generation
    :type name: str
    """
    claude.PLUGIN_MARKETPLACE_NAME = name
