"""
setup.py

define ``setup_claude_cli``, ``get_marketplace_folder_name``,
``get_surface_profiles``
"""

# pylint: disable=protected-access


import kamilog
from kaye_engine.cli import claude
from kaye_engine.consumer import get_consumer_canonical_name
from kaye_engine.prompt.affordance_registry import (
    register_variant,
    variant_registry,
)

__all__ = (
    "get_marketplace_folder_name",
    "get_surface_profiles",
    "setup_claude_cli",
)

# logger  ######################################################################
logger = kamilog.getLogger(claude.LOGGER_CLAUDE_NAME)


# Public API  ##################################################################


def setup_claude_cli(
    chat_exportable_name,
    merged_coder_exportable_name,
    affordance_groups=None,
    surface_profiles=None,
):
    """
    set every consumer-configurable value used by the ``claude`` CLI
    subcommand family in one call

    Prerequisite: :func:`register_consumer` (plugin, marketplace, and
    marketplace folder names, display name, and version derive from it),
    and :func:`register_exportable_entry` (or
    :func:`register_blueprint`) for ``chat_exportable_name`` and
    ``merged_coder_exportable_name``


    :param chat_exportable_name: registered name, in
            `exportable_registry`, of the Chat exportable
    :type chat_exportable_name: str
    :param merged_coder_exportable_name: registered name, in
            `exportable_registry`, of the Coder exportable carrying
            Chat as a dependency, used to build the final ``-c``
            prompt (``usp -c``, ``claude code``, ``claude
            vs-code-extension``)
    :type merged_coder_exportable_name: str
    :param affordance_groups: affordance canonical name -> its variant
            canonical names, registered via
            `register_claude_affordances`; a singleton affordance is
            simply a 1-tuple; defaults to ``None`` (treated as ``{}``)
    :type affordance_groups: dict[str, Iterable[str]] or None, optional
    :param surface_profiles: populates the ``--surface`` flag's
            choices; ``None`` (default) omits ``--surface`` entirely
    :type surface_profiles: dict[str, RenderProfile] or None, optional
    """
    claude._chat_exportable_name = chat_exportable_name
    claude._merged_coder_exportable_name = merged_coder_exportable_name
    claude._affordance_groups = affordance_groups or {}
    claude._surface_profiles = surface_profiles

    register_claude_affordances()


def register_claude_affordances():
    """
    register every name in the consumer-configured `affordance_groups`
    (see `setup_claude_cli`) into `variant_registry` via
    `register_variant`, skipping any `canonical_name` already
    registered -- keeps repeated `setup_claude_cli(...)` calls within
    one process idempotent instead of raising on the second call
    """
    for affordance_name, variant_names in claude._affordance_groups.items():
        for canonical_name in variant_names:
            if canonical_name in variant_registry:
                continue
            register_variant(canonical_name, affordance_name=affordance_name)


def get_marketplace_folder_name():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``register_consumer(...)``
    :return: marketplace folder name, the registered canonical name
    :rtype: str
    """
    return get_consumer_canonical_name()


def get_surface_profiles():
    """
    :return: configured ``dict[str, RenderProfile]`` populating the
            ``--surface`` flag's choices, or ``None`` when the consumer
            project never configured surfaces -- unlike this module's
            other getters, ``None`` is a valid, non-error configuration
            (precedented by ``default_surface=()`` for surface-less
            subcommands), so this never raises
    :rtype: dict[str, RenderProfile] or None
    """
    return claude._surface_profiles
